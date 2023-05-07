"""
@author: Kuro
"""

import aioredis
import asyncio
import async_timeout
import contextlib
from settings import Config


class RedisServices:

    def __init__(self):
        self.redis = None
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.init_redis())


    async def init_redis(self):
        """
        This is an asynchronous function that creates a Redis client using the aioredis library with the specified host and database.
        :return: The `init_redis` function is returning an instance of an `aioredis.Redis` object, which is created using the `aioredis.create_redis` method. This object represents a
        connection to a Redis server, which can be used to execute Redis commands and interact with the Redis data store.
        """
        self.redis = await aioredis.create_redis_pool(address=Config.redis_host, db=0)

    async def create_stream(self, name: str, fields: dict) -> str:
        """
        This Python function creates a Redis stream with a given name and fields if it does not already exist.

        :param name: A string representing the name of the stream to be created
        :type name: str
        :param fields: The `fields` parameter is a dictionary that contains the key-value pairs of the fields to be added to the stream. The keys represent the field names and the values
        represent the field values
        :type fields: dict
        :return: If the stream with the given name already exists, the function will return the string "Stream already exists". If the stream does not exist, the function will create a new
        stream with the given name and fields using the Redis `xadd` command, and return a string indicating that the stream was created with the given name and fields.
        """
        exists = await self.redis.exists(name)
        if exists:
            return "Stream already exists"
        await self.redis.xadd(name, fields)
        return f"Stream {name} created with fields {fields}"

    async def write_stream(self, name: str, fields: dict) -> str:
        """
        This Python function writes a dictionary of fields to a Redis stream and returns a confirmation message.

        :param name: The name parameter is a string that represents the name of the Redis stream to which the fields will be written
        :type name: str
        :param fields: The `fields` parameter is a dictionary that contains the data to be written to the Redis stream. The keys of the dictionary represent the field names, and the values
        represent the field values
        :type fields: dict
        :return: a string that indicates that the `fields` dictionary has been written to the Redis stream with the given `name`. The string includes the `fields` dictionary and the `name`
        of the stream.
        """
        await self.redis.xadd(name, fields)
        await self.redis.close()
        return f"{fields} writen to {name}"

    async def stream_info(self, stream: str) -> dict:
        """
        This Python function retrieves information about a Redis stream and returns it as a dictionary.

        :param stream: The `stream` parameter is a string that represents the name of the Redis stream for which we want to retrieve information
        :type stream: str
        :return: The function `stream_info` returns a dictionary containing information about the Redis stream specified by the `stream` parameter. The information is obtained using the
        `xinfo_stream` command from the Redis client library, and the function is an asynchronous function that uses the `await` keyword to wait for the response from Redis before
        returning the result. The Redis client connection is also closed after the response is obtained.
        """
        response = await self.redis.xinfo_stream(stream)
        await self.redis.close()
        return response

    async def delete_msg(self, stream: str, ids: list) -> str:
        """
        This is an asynchronous Python function that deletes messages with given IDs from a Redis stream and returns a confirmation message.

        :param stream: The name of the Redis stream from which the messages will be deleted
        :type stream: str
        :param ids: The `ids` parameter is a list of message IDs that need to be deleted from the Redis stream specified by the `stream` parameter
        :type ids: list
        :return: a string that says "msg id {id} on stream {stream} deleted", where {id} and {stream} are placeholders for the actual values passed as arguments to the function. However,
        there seems to be an error in the code as the variable "id" is not defined anywhere in the function. It should be replaced with "ids" to match the parameter name
        """
        await self.redis.xdel(stream, ids)
        await self.redis.close()
        return f"msg id {id} on stream {stream} deleted"

    async def delete_stream(self, name: str) -> str:
        """
        This Python function deletes a Redis stream with the given name and returns a message confirming the deletion.

        :param name: The name of the stream that needs to be deleted
        :type name: str
        :return: The function `delete_stream` returns a string that says "Stream {name} destroyed", where `{name}` is the value of the `name` parameter passed to the function.
        """
        await self.redis.delete(name)
        await self.redis.close()
        return f"Stream {name} destroyed"

    async def create_group(self, stream: str, group: str) -> str:
        """
        This is an asynchronous Python function that creates a Redis stream consumer group and returns a response message indicating whether the group was successfully created or not.

        :param stream: The name of the Redis stream on which the group is to be created
        :type stream: str
        :param group: The `group` parameter is a string representing the name of the consumer group that you want to create
        :type group: str
        :return: The function `create_group` returns a string that either confirms the successful creation of a Redis stream consumer group or provides an error message if the creation
        fails. The string will indicate the name of the stream and the name of the group that was created.
        """
        try:
            await self.redis.xgroup_create(stream, group)
            response = f"Group created on {stream} with name {group}"
        except exceptions.ResponseError as e:
            response = str(e)
        await self.redis.close()
        return response

    async def groups_info(self, stream: str) -> dict:
        """
        This Python function retrieves information about consumer groups from a Redis stream.

        :param stream: The `stream` parameter is a string that represents the name of the Redis stream for which we want to retrieve information about the consumer groups
        :type stream: str
        :return: The function `groups_info` returns a dictionary containing information about the consumer groups associated with the Redis stream specified by the `stream` parameter. The
        information is obtained using the `xinfo_groups` method of the Redis client object `redis`. The Redis client object is closed after the information is obtained.
        """
        response = await self.redis.xinfo_groups(stream)
        await self.redis.close()
        return response

    async def delete_group(self, stream: str, group: str) -> str:
        """
        This Python function deletes a Redis stream group and returns a confirmation message.

        :param stream: The name of the Redis stream from which the group needs to be deleted
        :type stream: str
        :param group: The `group` parameter is a string representing the name of the consumer group that needs to be deleted from the Redis stream specified by the `stream` parameter
        :type group: str
        :return: a string that says "Group {group} deleted on stream {stream}", where {group} and {stream} are the values passed as arguments to the function.
        """
        await self.redis.xgroup_destroy(stream, group)
        return f"Group {group} deleted on stream {stream}"

    async def consumers_info(self, stream: str, group: str) -> dict:
        """
        This Python function retrieves information about consumers in a Redis stream group.

        :param stream: The name of the Redis stream to retrieve consumer information from
        :type stream: str
        :param group: The `group` parameter is a string that represents the name of the consumer group for which we want to retrieve information. In Redis, a consumer group is a group of
        consumers that consume messages from a stream. The group ensures that each message is consumed by only one consumer in the group
        :type group: str
        :return: The function `consumers_info` returns a dictionary containing information about the consumers of a Redis stream in a specific consumer group. The information includes the
        name of each consumer, the number of pending messages for each consumer, and the idle time of each consumer.
        """
        return await self.redis.xinfo_consumers(stream, group)

    async def delete_consumer(self, stream: str, group: str, consumer: str) -> str:
        """
        This Python function deletes a consumer from a Redis stream group.

        :param stream: The name of the Redis stream from which the consumer
        needs to be deleted
        :type stream: str
        :param group: The name of the consumer group from which the consumer
        needs to be deleted
        :type group: str
        :param consumer: The `consumer` parameter is a string that represents
        the name of the consumer that needs to be deleted from a Redis Stream
        consumer group
        :type consumer: str
        :return: The function `delete_consumer` returns a string that says
        "Consumer {consumer} deleted on group {group}", where `{consumer}`
        and `{group}` are the values passed as
        arguments to the function.
        """
        await self.redis.xgroup_delconsumer(stream, group, consumer)
        return f"Consumer {consumer} deleted on group {group}"

    async def reader(self, channel):
        """
        This is an asynchronous function that continuously reads
        messages from a Redis Pub/Sub channel and prints them,
        until it receives a "STOP" message.

        :param channel: The `channel` parameter is an instance of the `aioredis.client.PubSub` class, which represents a Redis Pub/Sub channel. This channel can be used to publish messages
        to subscribers who have subscribed to the channel. The `reader` function is an asynchronous coroutine that reads messages from the
        :type channel: aioredis.client.PubSub
        """
        while True:
            with contextlib.suppress(asyncio.TimeoutError):
                async with async_timeout.timeout(1):
                    message = await channel.get_message(ignore_subscribe_messages=True)
                    if message is not None:
                        print(f"(Reader) Message Received: {message}")
                        if message["data"] == "STOP":
                            print("(Reader) STOP")
                            break
                    await asyncio.sleep(0.01)

    async def subscribe(self, channels: list):
        """
        This function subscribes to Redis pub/sub
        channels and creates a task to read messages from them.

        :param channels: A list of channel names to
        subscribe to in Redis pub/sub
        :type channels: list
        """
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(*channels)
        asyncio.create_task(self.reader(pubsub))

    async def publish(self, channels: list, message: dict):
        """
        This is an asynchronous Python function that publishes
        a message to one or more Redis channels.

        :param channels: A list of channel names to which the
        message should be published. These channels should already exist
        in the Redis server
        :type channels: list
        :param message: The `message` parameter is a dictionary that
        contains the data to be published to the specified channels. It
        could contain any key-value pairs that are relevant to
        the application's use case. The contents of the dictionary will
        be sent as a message to all the channels specified in the `channels` parameter
        :type message: dict
        """
        await self.redis.publish(*channels, message)

    async def consume_new_group_event(self, consumer: str, stream: str, group: str) -> list:
        """
        This function consumes new events from a Redis stream using the XREADGROUP command.

        :param consumer: The name of the consumer that wants to read messages from the stream
        :type consumer: str
        :param stream: The `stream` parameter is a string that represents the name of the Redis
        stream that the consumer wants to read from
        :type stream: str
        :param group: The `group` parameter is a string that represents the name of the consumer
        group that the consumer belongs to. In Redis, a consumer group is a group of consumers that
        consume messages from a stream. When a message is consumed by a consumer in a group, it is
        marked as read and is not
        :type group: str
        :return: The function `consume_new_group_event` returns a list of messages that have been
        consumed by the specified consumer from the specified stream in the specified group. The
        messages are returned as a list of tuples, where each tuple contains the ID of the message
        and a dictionary of its fields and values.
        """
        return await self.redis.xreadgroup(group, consumer, {stream: ">"})

    async def consume_pending_group_events(self, consumer: str, stream: str, group: str) -> list:
        """
        This function consumes pending events from a Redis stream for a specific consumer group.

        :param consumer: The name of the consumer that wants to read events from the stream
        :type consumer: str
        :param stream: The `stream` parameter is a string that represents the name of the Redis
        stream from which the consumer wants to read pending events
        :type stream: str
        :param group: The name of the consumer group that wants to consume events from the stream
        :type group: str
        :return: The function `consume_pending_group_events` returns a list of pending events from
        a Redis stream for a specific consumer group and stream. The events are consumed by the
        specified consumer and have not yet been acknowledged as processed.
        """
        return await self.redis.xreadgroup(group, consumer, {stream: "0"})

#
# class Register(object):
#     """
#     This class is used to register a function as a decorator. The function that is registered as a decorator will be called when the decorator is used on another function.
#     """
#     def __init__(self, **kwargs):
#         self.result = None
#         self.stream = kwargs.get("stream")
#         self.group = kwargs.get("group")
#         self.consumer = kwargs.get("consumer")
#
#     def __call__(self, fn):
#         async def wrap(*args, **kwargs):
#             await create_stream(self.stream, {"stream_created": True})
#             await create_group(self.stream, self.group)
#             kwargs["stream"] = self.stream
#             kwargs["group"] = self.group
#             kwargs["consumer"] = self.consumer
#             self.result = await fn(*args, **kwargs)
#             return self.result
#
#         return wrap
#
#
# async def ack_stream(stream: str, group: str, ids: list):
#     data = await redis.xack(stream, group, *ids)
#     return data
#
#
# async def handle_consumer_data(consumer_data: list, stream: str, group: str):
#     pending_ids = []
#     pending_data = []
#     for _, e in consumer_data:
#         for x in e:
#             pending_ids.append(x[0])
#             pending_data.append(x[1])
#     if pending_ids:
#         await ack_stream(stream, group, pending_ids)
#     return pending_data
