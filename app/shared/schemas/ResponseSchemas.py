from typing import Optional, List, Union, Any

from app.shared.schemas.orm_schema import ORMCamelModel


class BaseResponse(ORMCamelModel):
    """
    Base Response abstraction for standardized returns
    """

    success: bool
    error: Optional[str]
    response: Optional[Union[None, str, dict, List[dict]]]

    class Config:
        arbitrary_types_allowed = True


class GetObjectsResponse(BaseResponse):
    """
    GetObjectsResponse is a response object that
    contains a list of objects
    """

    response: List[Any]


class GetObjectResponse(BaseResponse):
    """
    GetObjectResponse is a response object that
    contains a single item in the response body
    """

    response: Any


class CloseObjectsResponse(BaseResponse):
    """
    It's a response object that tells the client what to
    expect when calling the `CloseObject` method.
    """

    pass


class CreateObjectResponse(BaseResponse):
    """
    CreateObjectResponse creates a response object for the given API request.
    """

    pass
