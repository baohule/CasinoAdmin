from typing import Any
import meilisearch
from uuid import UUID

from sqlalchemy import func

from app.shared.bases.base_model import ModelType
from app.shared.exception.utils import safe
from settings import Config

client = meilisearch.Client(Config.meilisearch_url, Config.meili_admin_key)


@safe
def add_user(user_id: str, **kwargs):
    """
    The add_user function adds a user to the users index.

    :param user_id:UUID: Used to Uniquely identify the user.
    :param username:str: Used to Store the username of the user that is being added.
    :param name:str: Used to Store the name of the user.
    :return: A list of the new user's id, username and name.
    """
    client.index("users").add_documents([dict(id=user_id, **kwargs)])


@safe
def update_user(user_id: str, **kwargs):
    """
    Args:
        user_id: The UUID of the user to update
        **kwargs: Any keywords whose values have changed
    """
    client.index("users").update_documents([dict(id=user_id, **kwargs)])


@safe
def remove_user(user_id: UUID):
    """
    The remove_user function removes a user from the database.

    :param user_id:UUID: Used to Specify the user that we want to remove from our database.
    :return: The user_id that was removed.
    """
    client.index("users").delete_document(str(user_id))


@safe
def search_users(model: ModelType, query: str) -> dict[str, Any]:
    """
    The search_users function searches the users index for any user that matches the query.
    It returns a list of all matching users.

    :param model: Model to pass down
    :param query:str: Used to Search for users by name.
    :return: A dictionary with the keys "success" and.

    """
    results = client.index("users").search(query)
    if users := results.get("hits"):
        user_ids = [user.get("id") for user in users]
        return {"success": True, "users": model.where(user_id__in=user_ids).all()}
    return {"success": False, "error": "No users found"}


def seed_users(users):
    client.index("users").add_documents(users)


def nuke_ms_db():
    client.index("users").delete_all_documents()
