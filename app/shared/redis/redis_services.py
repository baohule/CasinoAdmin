"""
@author: Kuro
"""
import json
from io import StringIO
from typing import Type, TypeVar, List, Optional, Any

import aioredis
import asyncio
import async_timeout
import contextlib

from aioredis import Redis
from py_linq import Enumerable
from py_linq.core import RepeatableIterable
from pydantic import BaseModel, BaseConfig, Field

from app.api.user.models import User
from app.api.user.schema import User as UserSchema
from app.rpc.game.schema import Session

from app.shared.middleware.json_encoders import ModelEncoder
from settings import Config


# from app import logging
#
# logger = logging.getLogger("redis_services")
#
# # logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)


class SocketSession(BaseModel):
    """
    The NestedSession class is used to represent a nested JSON object that is stored in Redis.
    """
    session_id: str
    session: Session


class Online(BaseModel):
    """
    The Online class is used to represent a list of users that are currently online.
    """
    users: List[UserSchema] = []


class Socket(BaseModel):
    """
    The Sessions class is used to represent a list of sessions that are currently active.
    """
    sessions: Optional[List[SocketSession]] = []


class Sockets(BaseModel):
    __root__: List[Socket] = []
    __self: __root__


T = TypeVar('T', bound=BaseModel)


class RedisMixin(BaseModel, Enumerable):
    """

    The goal of this model is to create an SQLALchemy-like redis mixin that
    gives us dot notation access and feature access to query our redis database.
    we do this with the py_linq lib's Enumerable which gives us a lot of the same
    features that SQLALchemy does. We also use the pydantic BaseModel to give us
    dot notation access to our redis database.

    """

    class Config(BaseConfig):
        arbitrary_types_allowed = True

    _instance: Any = None
    redis: Optional[Redis] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            self.__setattr__(k, v)

        # loop = asyncio.get_event_loop() or asyncio.new_event_loop()
        # loop.run_until_complete(self.init_redis())

    # def __new__(cls, **kwargs) -> Enumerable:
    #     # Singleton to avoid multiple connections to Redis
    #     if cls._instance is None:
    #         cls._instance = super().__new__(cls)
    #     return cls._instance

    @classmethod
    async def init_redis(cls):
        """
        This is an asynchronous function that creates a Redis client using the aioredis library with the specified host and database.
        :return: The `init_redis` function is returning an instance of an `aioredis.Redis` object, which is created using the `aioredis.create_redis` method. This object represents a
        connection to a Redis server, which can be used to execute Redis commands and interact with the Redis data store.
        """
        cls.redis = Redis(await aioredis.create_redis_pool(address=Config.redis_host, db=0))
        return cls.redis


    @classmethod
    async def read(cls, *args, **kwargs) -> Optional[T]:
        """
    The read function is used to read a single object from the database.
    It takes in any number of keyword arguments, and returns an instance of the
    class that called it if there is a match.
    If no match exists, None will be returned instead.

    Args:
        cls: Create a new instance of the class that called read
        *args: Accept any number of arguments
        **kwargs: Pass keyword arguments to the function

    Returns:
        The first object that matches the kwargs
"""
        redis_data = json.loads(await cls.redis.get(cls.__name__.lower()))
        print(redis_data)
        if not redis_data:
            return
        return (
            Enumerable(
                redis_data
        ).where(
            # Filter the list of objects to only include objects that have a key from kwargs
            lambda _object: any(
                _object.get(key) == value for key, value in kwargs.items()
            )
        )
                .first(lambda _object: _object and cls(**_object))
        )

    @classmethod
    async def read_all(cls, **kwargs):
        """
    The read_all function takes in a class and any number of keyword arguments.
    It then returns a list of objects that have the same key-value pairs as the kwargs passed in.

    Args:
        cls: Reference the class that is calling this function
        **kwargs: Pass in a dictionary of arguments

    Returns:
        A list of objects that match the kwargs passed to it

    """
        instance = cls()
        return (
            Enumerable(
                await instance.redis.get(
                    cls.__name__.lower()
                )
            ).where(
                # Filter the list of objects to only include objects that have a key from kwargs
                lambda _object: any(
                    _object.get(key) == value for key, value in kwargs.items()
                )
            )
            .select(lambda _object: _object and cls(**_object))
            .to_list()
        )

    @classmethod
    def filter_kwargs(cls, kwargs: dict, additional_filters: list = None):
        """
    The filter_kwargs function is used to remove any identity targets from the kwargs.
    This means that we would return only items that do not have id or _id in the kwargs,
    additionally we want to remove any items that have a value of None. This function is
    used by both create and update methods.

    Args:
        cls: Pass in the class that is being used to instantiate an object
        kwargs: Pass keyword arguments to a function

    Returns:
        A dictionary of key/value pairs that are not none


    """
        return {
            key: value for key, value in kwargs.items()
            if key and value
               and key in ["id", "_id", "Id"] or additional_filters and key in additional_filters
        }

    @classmethod
    async def update(cls, **kwargs):
        """
    The update function takes in a dictionary of key-value pairs and updates the
        object with those values. The function first filters out any keys that are not
        part of the class's schema, then it checks to see if an object exists with
        those filtered key-value pairs. If one does exist, it creates a new dictionary
        from that existing object and merges in the original kwargs passed into update().

    Args:
        cls: Pass the class object to the function
        **kwargs: Pass a variable number of keyword arguments to the function

    Returns:
        A class instance
    """
        instance = cls._instance
        target = cls.filter_kwargs(kwargs)
        if _object := await cls.read(**target):
            new_object = _object.dict()
            new_object.update(kwargs)
            await instance.redis.set(
                cls.__name__.lower(),
                new_object
            )
            return cls(**new_object)

    #@classmethod
    async def create(self, context: str = None, **kwargs):
        target = self.filter_kwargs(kwargs, additional_filters=["phone"])
        key = self.__class__.__name__.lower()
        redis = await self.init_redis()
        object_json = self.dict(exclude={'redis'}, exclude_none=True, exclude_unset=True)
        redis_data = await redis.get(key)

        async def _insert_key(node, data: dict = None):
            if isinstance(node, Enumerable):
                for child in node:
                    if isinstance(child, dict):
                        if all(item in child.items() for item in object_json.items()):
                            return
                    elif isinstance(child, Enumerable):
                        await _insert_key(child)
                if not any(isinstance(x, str) for x in node):
                    node.append(data)

        """
        data types in object oriented programming:
        
        
        hash: {'key': 'value'} -> {'name': 'mike'} 
        list: ['value1', 'value2'] -> ['mike', 'joe']
        set: {'value1', 'value2'} -> {'mike', 'joe'}
        sorted set: {'value1': 1, 'value2': 2} -> {'mike': 1, 'joe': 2}
        now lets explain hashes vs binanry tree vs linked list
        hash is a single item with a key value structure
        a binary tree is a data structure that has a root node and two children nodes
        a linked list is a data structure that has a head node and a tail node
        
        [             
            { 1: {
            
                "person1": {
                        "thisngh1": "none",
                        "thign2": {
                                ...
                            }
                },
                "person2": "none"
        },             
            { 2: {
            
                "person1": {
                    
                },
                "person2": {
                   
            }
        }
    ]
        
            
            
            
        
        
        
        """





        if redis_data:
            master_object = Enumerable(json.loads(redis_data))
            await _insert_key(master_object, object_json)
            await redis.set(key, json.dumps(master_object.to_list()))
        else:
            master_object = [object_json]
            await redis.set(key, json.dumps(master_object))

        return self.__class__(**kwargs)

        # if not await cls.read(**target)
        #     await cls.redis.set(
        #         cls.__name__.lower(),
        #         json.dumps([cls.json()])
        #     )
        #     return cls(**kwargs)


class SomeModel(RedisMixin):
    id: Optional[int]
    name: Optional[dict]
    age: Optional[int]


async def print_model():
    model = SomeModel(id=1, name={"first": "mike", "last": "brown"}, age=20)
    await model.init_redis()
    await model.create(context="users")


asyncio.run(print_model())

#
# class RedisCRUD:
#     """
#     The RedisCRUD class is a generic class that can be used to perform CRUD operations on Redis.
#     """
#
#     def __init__(self, redis_client: Redis):
#         self.redis = redis_client
#
#     # async def get(self, key: str, model_cls: Type[T] = None) -> Optional[Any]:
#     #     """
#     # The get function takes a key and a model class as arguments.
#     # It then attempts to retrieve the data from Redis using the given key.
#     # If it succeeds, it parses that data into an instance of the given model class and returns that instance.
#     # Otherwise, if no such value exists in Redis for this key, None is returned.
#     #
#     # Args:
#     #     self: Represent the instance of the class
#     #     key: str: Specify the key of the data to be retrieved
#     #     model_cls: Type[T]: Specify the type of the object that will be returned
#     #
#     # Returns:
#     #     An instance of the model_cls class if data is not none
#     #
#     # """
#     #     data = self.redis.get(key)
#     #     if data is None:
#     #         return None
#     #
#     #     # if isinstance(data, dict):
#     #     #     return model_cls(**{k: self.get(k, v) for k, v in data.items()})
#     #     #
#     #     # if isinstance(data, list):
#     #     #     return [json.dumps(item) for item in data]
#     #     json_data = json.loads(data)
#     #     if isinstance(model_cls, Sockets):
#     #         return Sockets(*json_data)
#     #
#     #     if isinstance(json_data, list):
#     #         return [model_cls.parse_raw(item) for item in json_data]
#     #
#     #     # loaded_json = [json.loads(item) for item in json_data if item]
#     #     logger.info(json_data)
#     #     return model_cls(**json_data)
#
#     async def set(self, key: str, value) -> None:
#         """
#     The set function takes a key and value as parameters.
#     The value is converted to JSON, then the key and data are passed to Redis's set function.
#
#     Args:
#         self: Represent the instance of the object itself
#         key: str: Set the key of the value
#         value: T: Type check the value being set
#
#     Returns:
#         None
#
#     """
#         data = json.dumps(value, cls=ModelEncoder)
#         self.redis.set(key, data)
#
#     async def delete_session_child(self, redis_key: str, lookup_key: str, lookup_value: str) -> None:
#         """
#     The delete_child function is used to delete a child object from a parent object.
#
#     Args:
#         self: Reference the instance of the class
#         redis_key: str: Specify the key in redis that we want to delete a child from
#         lookup_key: str: Find the item to delete
#
#     Returns:
#         None, but it should return the items_clean variable
#
#     """
#         redis_items: Enumerable = await self.get_sessions()
#         print(redis_items)
#         items_clean = Socket(
#             sessions=redis_items.where(
#                 lambda item: item.dict().get(lookup_key) != lookup_value
#             ).to_list()
#         )
#         await self.redis.set(redis_key, items_clean.sessions)
#
#     async def list(self, prefix: str, model_cls: Type[T]) -> List[T]:
#         """
#     The list function returns a list of all objects in the database that match
#     the given prefix. The model_cls argument is used to determine which class to
#     use when deserializing the object from JSON.
#
#     Args:
#         self: Represent the instance of the class
#         prefix: str: Specify the prefix of the keys that will be returned
#         model_cls: Type[T]: Specify the type of model class that will be returned
#
#     Returns:
#         A list of all the keys that match the prefix
#
#     """
#         keys = await self.redis.keys(f'{prefix}*')
#         return [await self.get(key, model_cls=model_cls) for key in keys]
#
#     async def get_sessions(self) -> Optional[Enumerable]:
#         """
#         The get_session_children function takes a key as an argument and returns a Session object
#         if the key exists in Redis. Otherwise, it returns None.
#         """
#         sockets = Enumerable(await self.get('sockets', Sockets))
#         logger.info(sockets)
#
#         return sockets
#
#     async def get_session(self, lookup_key: str = None, session_id: str = None) -> Optional[SocketSession]:
#         """
#         The get_session function takes a key as an argument and returns a Session object
#         if the key exists in Redis. Otherwise, it returns None.
#         """
#         sessions: Enumerable = await self.get_sessions()
#         redis_item = sessions.first(lambda item: item.session.get(lookup_key))
#         if session_id:
#             redis_item = sessions.first(lambda item: item.session_id == session_id)
#
#         return redis_item and Session.construct(redis_item)
#
#     async def get_online_users(self) -> Online:
#         """
#         The get_session function takes a key as an argument and returns a Session object
#         if the key exists in Redis. Otherwise, it returns None.
#         """
#
#         return Online(users=await self.list('user:', UserSchema))
#
#     async def get_user(self, phone: str) -> Optional[UserSchema]:
#         """
#     The get_user function returns a user object from the online_users table.
#         Args:
#             phone (str): The phone number of the user to be returned.
#
#     Args:
#         self: Refer to the class itself
#         phone: str: Specify the type of data that will be passed to the function
#
#     Returns:
#         The first user in the list of users that matches the phone number
#     """
#         online = await self.get('online_users', model_cls=Online)
#         users = Enumerable(online.users)
#         return users.first(lambda x: x.phone == phone)
#
# #
# # class Register(object):
# #     """
# #     This class is used to register a function as a decorator. The function that is registered as a decorator will be called when the decorator is used on another function.
# #     """
# #     def __init__(self, **kwargs):
# #         self.result = None
# #         self.stream = kwargs.get("stream")
# #         self.group = kwargs.get("group")
# #         self.consumer = kwargs.get("consumer")
# #
# #     def __call__(self, fn):
# #         async def wrap(*args, **kwargs):
# #             await create_stream(self.stream, {"stream_created": True})
# #             await create_group(self.stream, self.group)
# #             kwargs["stream"] = self.stream
# #             kwargs["group"] = self.group
# #             kwargs["consumer"] = self.consumer
# #             self.result = await fn(*args, **kwargs)
# #             return self.result
# #
# #         return wrap
# #
# #
# # async def ack_stream(stream: str, group: str, ids: list):
# #     data = await redis.xack(stream, group, *ids)
# #     return data
# #
# #
# # async def handle_consumer_data(consumer_data: list, stream: str, group: str):
# #     pending_ids = []
# #     pending_data = []
# #     for _, e in consumer_data:
# #         for x in e:
# #             pending_ids.append(x[0])
# #             pending_data.append(x[1])
# #     if pending_ids:
# #         await ack_stream(stream, group, pending_ids)
# #     return pending_data
