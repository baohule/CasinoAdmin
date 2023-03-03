"""
@author: Kuro
"""
from fastapi import APIRouter, Depends, Request
from app.api.user.models import User
from app.shared.middleware.auth import JWTBearer
from app.api.user.schema import AdminUserCreate
import app.api.admin.schema as schema
from app.api.admin.models import AdminUser, AdminRole
from fastapi.logger import logger
from fastapi.exceptions import HTTPException

router = APIRouter(
    prefix="/api/admin",
    dependencies=[Depends(JWTBearer(admin=True))],
    tags=["admin"],
)

NO_PERMS = "Insufficient role permissions to access this endpoint"
NO_ROLE = "No Role Access"


@router.post("/manage/create_user", response_model=schema.Response)
async def create_user(user: AdminUserCreate, request: Request):
    """

    The create_user function creates a new user in the database.
    It takes in a UserCreate object and returns a dictionary with two keys: success and response.
    The success key is True if the user was created, False otherwise. The response key contains either an
    error message or information about the newly created user.

    Phone number will accept any form as long as it starts with a +1.
    Birthday has to be in format year-month-day.

    :param user:UserCreate: Used to Pass in the data that is being.
    :param request:Request: Used to Get the user's role.
    :return: A dictionary with a key of 'success' and either true or false as the value.


    """

    role = request.user.admin_role
    if not role or not role.can_create:
        return {"success": False, "error": NO_ROLE}

    user_data = user.dict()
    create = User.create_user(**user_data)
    return (
        {"success": True, "response": f"{user.username} added to database"}
        if create
        else {"success": False, "response": "user not created"}
    )


@router.post("/manage/create_admin", response_model=schema.Response)
async def create_admin(user: AdminUserCreate, request: Request):
    """
    The create_admin function creates a new admin in the database.
    It takes in a UserCreate object and returns a dictionary with either success: True or error: <error message>.
    The create_user function requires an AdminUser role to execute.

    :param user:UserCreate: Used to Specify the type of data that is being passed to the function.
    :param request:Request: Used to Get the current user.
    :return: A dictionary with the key "success" set to true or false.


    """
    """
    Phone number will accept any form as long as it starts with a +1.
    Birthday has to be in format year-month-day.
    """

    role = request.user.admin_role

    if not role or not role.can_create:
        return {"success": False, "error": NO_ROLE}

    created = AdminUser.add_admin(**user.dict())
    return (
        {"success": True, "response": f"{user.username} added to database"}
        if created
        else {"success": False, "response": "user not created"}
    )


@router.post("/manage/update_user", response_model=schema.Response)
async def update_user(user: schema.BaseUser, request: Request):
    """
    The update_user function updates a user's information.
    It takes in the following parameters:
        - user: The schema object of the user to be updated.
        - request: The request object containing all data sent by client, including session cookie and form data.

        It returns a dictionary with two keys, success and response.  If successful, success is True and response
        contains no value (empty string). Otherwise, success is False and response contains an error message.

         Phone number can be any form as long as it exists in the db.

    :param user:schema.BaseUser: Used to Pass in the user object.
    :param request:Request: Used to Get the user id of the current logged in user.
    :return: A dictionary with the success key set to true or false depending on whether it was.

    """
    role = request.user.admin_role
    if not role or not role.can_alter_user:
        return {"success": False, "error": NO_ROLE}

    data = user.dict(exclude_unset=True)
    update = User.update_user(**data)
    return (
        {"success": True, "response": f"user {user.id} updated"}
        if update
        else {"success": False, "response": "user not updated"}
    )


@router.post("/manage/remove_user", response_model=schema.Response)
async def remove_user(user: schema.RemoveUser, request: Request):
    """
    The remove_user function removes a user from the database.
    It takes in a request object and an id of the user to be removed.
    If there is no such user, it returns false.

    :param user:schema.RemoveUser: Used to Pass the id of the user to be removed.
    :param request:Request: Used to Get the user id of the logged-in user.
    :return: A dictionary with the key "success" and a boolean value.

 
    """
    role = request.user.admin_role
    if not role or not role.can_alter_user:
        return {"success": False, "error": NO_ROLE}

    remove = User.remove_user(id=user.id)
    return (
        {"success": True, "response": f"user {user.id} removed"}
        if remove
        else {"success": False, "response": "user not removed"}
    )


@router.post("/list_users", response_model=schema.ListUserResponse)
async def list_users(context: schema.GetUserList, request: Request):
    """
    The list_users function returns a list of all users in the system.

    This function requires admin privileges to run.

    :param context:schema.GetUserList: Used to Pass in the request object.
    :param request:Request: Used to Pass in the current request.
    :return: A list of users.
    """
    role = request.user.admin_role
    if not role or not role.can_list_users:
        return HTTPException(401, detail=NO_PERMS)
    return User.get_all_users(context.params.page, context.params.size)


@router.post("/get_user", response_model=schema.BaseUserResponse)
async def get_user(user: schema.User, request: Request):
    """
    The get_user function is a ReST function that takes in a user object and returns the corresponding AdminUser object.
    It does this by checking if the user is an admin, and then returning the corresponding AdminUser object. If they are not
    an admin, it will return an HTTPException with status code 401 (unauthorized)

    :param user:schema.User: Used to Get the user from the database.
    :param request:Request: Used to Get the user from the request.
    :return: The user object if the user exists.
    """
    role = request.user.admin_role
    if not role or not role.can_list_users:
        return HTTPException(401, detail=NO_PERMS)

    if user := AdminUser.get_admin_by_id(user_id=user.id):
        return user
    return {"success": False}


@router.post("/search_users", response_model=schema.SearchResults)
async def search_users(dataset: schema.SearchUsers, request: Request):
    """
    The search_users function searches for users in the database.
    It accepts a list of dictionaries, each dictionary containing search parameters.
    Each dictionary is searched independently and the results are merged together.
    The keys of each dictionary should be one or more fields from the User model, and their values should be strings to search for.

     Phone number can be any form as long as it exists in the db.

    :param dataset:schema.SearchUsers: Used to Pass the data to the function.
    :param request:Request: Used to Access the user object.
    :return: A list of users that match the search criteria.
    """
    role = request.user.admin_role
    if not role or not role.can_search_users:
        return HTTPException(401, detail=NO_PERMS)

    results = {}
    for index, query in enumerate(dataset.__root__):
        users: list = User.admin_search_users(**query.dict())
        results[index] = users
    return results


@router.post("/manage/batch_delete_users", response_model=schema.Response)
async def batch_delete_users(dataset: schema.SearchUsers, request: Request):
    """
    The batch_delete_users function removes users from the database.

    :param dataset:schema.SearchUsers: Used to Pass in the data that we want to use for the batch delete.
    :param request:Request: Used to Get the user object of the request.
    :return: A httpException with a 401 status code.

     Phone number can be any form as long as it exists in the db.
    """

    role = request.user.admin_role
    if not role or not role.can_batch_alter_users:
        return HTTPException(401, detail=NO_PERMS)

    for query in dataset.__root__:
        removed = User.remove_user(id=query.id)
        if not removed:
            logger.info(f"{query.id} failed")
    return {"success": True}


@router.post("/manage/batch_update_users", response_model=schema.Response)
def batch_update_users(dataset: schema.BatchUsers, request: Request):
    """
    The batch_update_users function is used to update multiple users at once.
    It takes in a list of dictionaries, each dictionary containing the user's information.
    The function then iterates through the list and updates each user accordingly.

      Phone number can be any form as long as it exists in the db.

    :param dataset:schema.BatchUsers: Used to Pass in a list of dictionaries that represent the data to be updated.
    :param request:Request: Used to Get the user information.
    :return: A boolean value.
    """

    role = request.user.admin_role
    if not role or not role.can_batch_alter_users:
        return HTTPException(401, detail=NO_PERMS)
    for query in dataset.__root__:
        data: dict = query.dict()
        updated = User.update_user(**data)
        if not updated:
            logger.info(f"{query} failed to update")

    return {"success": True}


@router.post("/manage/update_user_role", response_model=schema.SetUserRoleResponse)
def update_user_role(context: schema.SetUserRole, request: Request):
    """
    The update_user_role function updates the role of a user.

    :param context:schema.SetUserRole: Used to Specify the user to change.
    :param request:Request: Used to Get the user object.
    :return: A HTTPException with a 401 status code and the message
    "you do not have permission to perform this action.


    """
    role = request.user.admin_role
    if not role or not role.can_set_perms:
        return HTTPException(401, detail=NO_PERMS)

    success = AdminRole.set_user_role(user_id=context.user_id, user_role=context.role)
    return {"success": success}


@router.post("/manage/update_roles", response_model=schema.SetPermsResponse)
def update_roles(context: schema.SetPerms, request: Request):
    """
    The update_roles function takes a request object and a context dictionary.
    It then checks to see if the user has permission to set permissions on an admin role,
    and if so, it updates the roles of that admin role with the new roles in the context dictionary.

    :param context:schema.SetPerms: Used to Specify the object that is being updated.
    :param request:Request: Used to Get the current user.
    :return: True if the user is an admin and has permission to set permissions.


    """
    role = request.user.admin_role
    if not role or not role.can_set_perms:
        return HTTPException(401, detail=NO_PERMS)

    success = AdminRole.alter_role_perms(**context.dict())
    return {"success": success}


@router.post("/set_admin_name", response_model=schema.AdminUserUpdateNameResponse)
async def set_admin_name(context: schema.AdminUserUpdateName, request: Request):
    """
    The set_admin_name function updates the name of an admin user.

    :param context:schema.AdminUserUpdateName: Used to Update the name of an admin user.
    :param request:Request: Used to Get the user id from the request.
    :return: A dictionary with a key of "success" and either true or false as the value.
    """
    new_name = context.dict()
    admin_id = request.user.id
    user = AdminUser.get_admin_by_id(admin_id)

    if not user:
        return {"success": False, "error": "User not found"}

    new_name["id"] = admin_id
    if AdminUser.update_admin_user(**new_name):
        return {"success": True}
    return {"success": False, "error": "Unable to update record"}
