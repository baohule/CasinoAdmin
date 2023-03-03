import math
import uuid
from datetime import datetime
from operator import or_
from types import SimpleNamespace
from typing import Type, Union, Tuple, List, Any, Generic
from typing import TypeVar

import pytz
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from sqlalchemy import func, and_
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.engine import Row
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import registry, Query
from sqlalchemy_mixins.activerecord import ActiveRecordMixin
from sqlalchemy_mixins.inspection import InspectionMixin
from sqlalchemy_mixins.smartquery import SmartQueryMixin
from starlette.requests import Request
from typing_extensions import T

from app.shared.exception.exceptions import PredicateConditionException

mapper_registry = registry()
DeclarativeBase = declarative_base()
Base = mapper_registry.generate_base(
    cls=(DeclarativeBase, ActiveRecordMixin, SmartQueryMixin, InspectionMixin)
)
ModelType = TypeVar("ModelType", bound=Base)


@mapper_registry.mapped
class ModelMixin(Base):
    """
    Generic Mixin Model to provide helper functions that all Model classes need
    """

    __abstract__ = True

    @classmethod
    def get_or_create(cls: ModelType, *_, **kwargs) -> ModelType:
        """
        The get_or_create function is a helper function that will either get an object or create it if it doesn't exist.
        For example, let's say we have a model called User with two fields: username and email.
        We want to be able to easily create new users based on their username and email address, but we also
        want our API endpoints (and other parts of our code) to check whether a user already exists before creating them.

        :param cls:ModelType: Used to Specify the model class that will be used to create or retrieve an instance.
        :param *_: Used to Ignore the first positional argument.
        :param **kwargs: Used to Pass in all the fields of the model.
        :return: A tuple containing the object and a boolean value indicating whether it was created.
        """
        return cls.find(kwargs.get("id")) or cls.create(**kwargs)

    @classmethod
    def map_to_model(cls, model: Type[BaseModel], db_response: Union[Row, List[Row]]):
        """
        The map_to_model function takes a model and a list of tuples,
        and returns the same list of tuples with each tuple converted into an instance
        of the given model. For example:

            map_to_model(User, [('user-id', 'username'), ('user-id2', 'username2')])
            # Returns [User(user_id='user-id', username='username'), User(...)]

        :param model:Type[BaseModel]: Used to Specify the model that is used to create a list of instances.
        :param db_response:Union[Row: Used to Determine if the db_response is a list of keyed tuples or just one.
        :param List[Row]]: Used to Check if the db_response is a list of keyed tuples.
        :return: An instance of the model class with properties mapped to value from the db_response.
        """

        def mapper(tuple_data: Row) -> BaseModel:
            """
            The mapper function takes a tuple of data which is keyed and returns a dictionary.

                {'id': '<id>', 'name': '<name>', ...}

            Each key-value pair in this returned dictionary corresponds to one column
            in the database schema

            :param tuple_data:Row: Used to Pass in the data that is being mapped.
            :return: A dictionary with the key being the name of the column, and the value the row
            """
            zipped_tuples = dict(zip(tuple_data.keys(), tuple_data))
            return model(**zipped_tuples)

        if isinstance(db_response, list):
            return [mapper(item) for item in db_response]
        return mapper(db_response)

    @classmethod
    def rebuild(cls, kwargs: dict) -> dict:
        """
        The rebuild function takes a dictionary of data and returns a new dictionary
        with the following changes:
            - The created_at field is set to the current time.
            - If an id value is not provided, one will be generated.

            Args:
                kwargs (dict): A dictionary of data to rebuild into a model instance.

            Returns:
                dict: A rebuilt model instance with all fields updated and any missing ids added.

        :param kwargs:dict: Used to Pass in the dictionary of arguments that is being passed into the function.
        :return: A dictionary.
        """
        timestamp = datetime.now(pytz.utc)
        new_kwargs = dict(kwargs)
        new_kwargs["created_at"] = timestamp
        if not new_kwargs.get("id"):
            item_id = uuid.uuid4()
            new_kwargs["id"] = item_id
        return new_kwargs

    @classmethod
    def build_filters(cls, kwargs: dict, constraints: list = None) -> dict:
        """
        The build_filters function takes a dictionary of keyword arguments and returns a dictionary of
        filters that can be used to query the database. The returned filters are constrained by the
        keyword arguments passed in, which are also used as the keys for the returned filters. If no
        constraints are provided, all keyword arguments will be used as constraints.

        :param kwargs:dict: Used to Pass in the dictionary of parameters that we want to filter on.
        :param constraints:list=None: Used to Specify which constraints to apply.
        :return: A dictionary of filters.
        """
        if not constraints:
            constraints = list(kwargs.keys())
        return {k: v for k, v in kwargs.items() if k in constraints}

    @classmethod
    def get_filters(cls, context: BaseModel = None, kwargs: dict = None):
        """
        The get_filters function is a helper function that takes in the context and kwargs
        and returns a dictionary of filters. The get_filters function is used by all the
        endpoints to filter their results.

        :param context:BaseModel=None: Used to Pass the context of the request.
        :param kwargs:dict=None: Used to Pass in any additional keyword arguments that are passed into the function.
        :return: A dictionary of filters.
        """
        filters = kwargs
        if isinstance(context, BaseModel):
            filters["context"] = context.dict(exclude_unset=True)
        return filters

    @classmethod
    def get_owner_context(
            cls, request: Request, context: BaseModel
    ) -> Tuple[UUID, dict]:
        """
        The get_owner_context function accepts a request and context object as arguments.
        It returns the owner_id of the user making the request, and a dictionary containing
        the values from the context object that are not None or empty strings.

        :param request:Request: Used to Get the user id of the current logged-in user.
        :param context:BaseModel: Used to Get the fields of the model that are not none or empty strings.
        :return: The owner_id of the user making the request, and a dictionary containing.
        """
        owner_id: UUID = request.user.id
        context_dict = context.dict(exclude_unset=True)
        context_dict["owner_id"] = owner_id
        return owner_id, context_dict

    @classmethod
    def get_kwarg_dependencies(cls, kwargs):
        """
        The get_kwarg_dependencies function takes a dictionary of keyword arguments and removes any keyword
        arguments that do not contain an _id field, which is the default requirement of any user identity object.

        :param kwargs: Used to Store the arguments passed to a function.
        :return: A list of the dependencies for a given kwarg.
        """
        return [k for k in list(kwargs.keys()) if "_id" in k]

    @staticmethod
    def get_id_args(cls, *_, **kwargs):
        return {k: v for k, v in kwargs.items() if v and "_id" in k}

    @staticmethod
    def check_many_conditions(_or_: Union[list, dict] = None, _and_: list = Union[list, dict]):
        """
        The check_many_conditions function checks to see if the conditions are met.
        It takes two arguments, _or_ and _and_. If both arguments are lists, it checks to see if
        either of the conditions in the list is true. If only one argument is a list, it checks
        to see if all the conditions in that list are true. If neither argument is a list, then
        check_many_conditions returns the input in a dictionary format

        :param _or_:Union[list: Used to Define a list of conditions that are all required to be true.
        :param dict]=None: Used to Check if the _or_ parameter is a list.
        :param _and_:list=Union[list: Used to Make sure that the _and_ parameter is a list.
        :param dict]: Used to Store the conditions that are to be checked.
        :return: A dictionary with the keys being the _and_ conditions and values being either a list of _or_
                conditions or a single _or_ condition.

        """

        if isinstance(_and_, list) and isinstance(_or_, list):
            raise PredicateConditionException

        if isinstance(_or_, list):
            return {and_: _or_}
        if isinstance(_and_, list):
            return {or_: _and_}
        return {or_: _and_ or _or_, and_: _or_ or _and_}

    @staticmethod
    def get_constraints(kwargs, constraints: List[str]):
        """
        It takes a dictionary of keyword arguments and a list of constraints, and returns a SimpleNamespace object with only the keys that are in the constraints list

        :param kwargs: The keyword arguments passed to the function
        :param constraints: A list of strings that represent the constraints that you want to be able to pass in
        :type constraints: List[str]
        :return: A SimpleNamespace object with the keys and values of the kwargs dictionary.
        """
        return SimpleNamespace(
            **{k: v or None for k, v in kwargs.items() if k in constraints}
        )

    @classmethod
    def build_response(
            cls: ModelType = None,
            object_data: Any = None,
            error: str = None,
            overload: dict = None,
    ) -> dict:
        """
        The build_response function takes a list of database objects and returns a dictionary with the following structure:

        "success": True, or False if no data was returned from the database.
        "<Model Name>": [<database object>] The actual data that was returned from the database.
        :param overload: custom dictionary to overload the response with
        :param error: Custom Error message if any
        :param object_data: Optional data to include in the response
        :param cls: Used to Access variables that belongs to the class.
        :return: A dictionary with a key of success and the data.
        """
        if overload:
            return dict(success=True, error=None, response=None, **overload)

        if cls:
            return {
                "success": True,
                "response": object_data or cls,
            }
        return {
            "success": False,
            "error": error
                     or f"unable to perform crud operation on {object_data or 'object'}",
        }


class Page(Generic[T]):
    """
    Pagination class to allow for paging of database data
    """

    def __init__(self, items, page, page_size, total):
        self.items = items
        self.dict_items = [item._asdict() for item in items]
        self.page = page
        self.page_size = page_size
        self.total = total
        self.previous_page = None
        self.next_page = None
        self.has_previous = page > 1
        if self.has_previous:
            self.previous_page = page - 1
        previous_items = (page - 1) * page_size
        self.has_next = previous_items + len(items) < total
        if self.has_next:
            self.next_page = page + 1
        self.pages = int(math.ceil(total / float(page_size)))

    def __getitem__(self, parameters):
        return self._getitem(self, parameters)

    def as_dict(self):
        """
        The as_dict function returns a dictionary representation of the object.
        This is useful for JSON serialization, and also allows you to access all the
        properties on the object directly from the returned dictionary.

        :param self: Used to Reference the current instance of the class.
        :return: A dictionary that contains all the information about the object.
        """
        return self.__dict__

    def _getitem(self, self1, parameters):
        """
        The _getitem function is a helper function that is called by the getitem method.
        It takes in two parameters, self and parameters. The self parameter is automatically passed to the function when it's called, so you don't need to worry about this one too much. The second parameter is a dictionary of all of the keyword arguments that were passed into getitem (which was itself called from __getitem__). This means that if someone calls your class like:

        my_class["hello", "world"]  # <- This will be translated into `my_class._getitem({"key": ["hello", "world"]})` by Python before calling __getitem__.

        :param self: Used to Access variables that belongs to the class.
        :param self1: Used to Refer to the instance of the class.
        :param parameters: Used to Pass in the parameters of the function.
        :return: A list of the items in the set.
        """


def paginate(query: Query, page: int, page_size: int) -> Page[Row]:
    """
    The paginate function takes a query, the page number and page size as arguments.
    It then returns a tuple of the items on that page and the total number of items.

    :param query: Used to Pass a query object to the paginate function.
    :param page: Used to Determine which page of results to return.
    :param page_size: Used to Determine how many items to show on each page.
    :return: A tuple containing the list of items for that page, and a total number of pages.
    """
    if page <= 0:
        raise HTTPException(400, detail="page needs to be >= 1")
    if page_size <= 0:
        raise HTTPException(400, detail="page_size needs to be >= 1")
    items: list[Row] = query.limit(page_size).offset((page - 1) * page_size).all()
    total = query.select(func.count(1)).first()
    return Page(items, page, page_size, total)
