"""
@author: Kuro
"""
import aioredis
import asyncio
import async_timeout
from settings import Config

redis = aioredis.from_url(Config.redis_host, encoding="utf-8", decode_responses=True)


async def create_stream(name: str, fields: dict) -> str:
    exists = await redis.exists(name)
    if exists:
        return "Stream already exists"
    if not exists:
        await redis.xadd(name, fields)
        return f"Stream {name} created with fields {fields}"
    await redis.close()


async def write_stream(name: str, fields: dict) -> str:
    await redis.xadd(name, fields)
    await redis.close()
    return f"{fields} writen to {name}"


async def stream_info(stream: str) -> dict:
    response = await redis.xinfo_stream(stream)
    await redis.close()
    return response


async def delete_msg(stream: str, ids: list) -> str:
    await redis.xdel(stream, ids)
    await redis.close()
    return f"msg id {id} on stream {stream} deleted"


async def delete_stream(name: str) -> str:
    await redis.delete(name)
    await redis.close()
    return f"Stream {name} destroyed"


async def create_group(stream: str, group: str) -> str:
    try:
        await redis.xgroup_create(stream, group)
        response = f"Group created on {stream} with name {group}"
    except exceptions.ResponseError as e:
        response = str(e)
    await redis.close()
    return response


async def groups_info(stream: str) -> dict:
    response = await redis.xinfo_groups(stream)
    await redis.close()
    return response


async def delete_group(stream: str, group: str) -> str:
    await redis.xgroup_destroy(stream, group)
    return f"Group {group} deleted on stream {stream}"


async def consumers_info(stream: str, group: str) -> dict:
    response = await redis.xinfo_consumers(stream, group)
    return response


async def delete_consumer(stream: str, group: str, consumer: str) -> str:
    await redis.xgroup_delconsumer(stream, group, consumer)
    return f"Consumer {consumer} deleted on group {group}"


async def reader(channel: aioredis.client.PubSub):
    while True:
        try:
            async with async_timeout.timeout(1):
                message = await channel.get_message(ignore_subscribe_messages=True)
                if message is not None:
                    print(f"(Reader) Message Received: {message}")
                    if message["data"] == "STOP":
                        print("(Reader) STOP")
                        break
                await asyncio.sleep(0.01)
        except asyncio.TimeoutError:
            pass


async def subscribe(channels: list):
    pubsub = redis.pubsub()
    await pubsub.subscribe(*channels)
    asyncio.create_task(reader(pubsub))


async def publish(channels: list, message: dict):
    await redis.publish(*channels, message)


async def consume_new_group_event(consumer: str, stream: str, group: str) -> list:
    response = await redis.xreadgroup(group, consumer, {stream: ">"})
    return response


async def consume_pending_group_events(consumer: str, stream: str, group: str) -> list:
    response = await redis.xreadgroup(group, consumer, {stream: "0"})
    return response


class Register(object):
    def __init__(self, **kwargs):
        self.result = None
        self.stream = kwargs.get("stream")
        self.group = kwargs.get("group")
        self.consumer = kwargs.get("consumer")

    def __call__(self, fn):
        async def wrap(*args, **kwargs):
            await create_stream(self.stream, {"stream_created": True})
            await create_group(self.stream, self.group)
            kwargs["stream"] = self.stream
            kwargs["group"] = self.group
            kwargs["consumer"] = self.consumer
            self.result = await fn(*args, **kwargs)
            return self.result

        return wrap


async def ack_stream(stream: str, group: str, ids: list):
    data = await redis.xack(stream, group, *ids)
    return data


async def handle_consumer_data(consumer_data: list, stream: str, group: str):
    pending_ids = []
    pending_data = []
    for _, e in consumer_data:
        for x in e:
            pending_ids.append(x[0])
            pending_data.append(x[1])
    if pending_ids:
        await ack_stream(stream, group, pending_ids)
    return pending_data
