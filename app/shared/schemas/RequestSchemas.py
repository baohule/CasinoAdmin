from typing import Optional
from uuid import UUID

from fastapi_camelcase import CamelModel


class BaseRequest(CamelModel):
    """
    Request factory for our abstract input class
    """

    primary_key: UUID
    optional_key: Optional[UUID]

    class Config:
        """
        Base Config Object with example
        """

        schema_extra = {
            "example": {
                "userId": "eb773795-b3a2-4d0e-af1d-4b1c9d90ae26",
            }
        }


class GetObjects(BaseRequest):
    """
    GetObjects represents a generic getter for a list of objects
    to be fetched from the database with a single common key.
    """

    pass


class CloseObject(BaseRequest):
    """
    CloseObject exists as an abstract input schema to mark
    and object inactive in the database.
    """

    pass
