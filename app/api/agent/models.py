"""
@author: Kuro
"""
import datetime
import uuid
import pytz
from sqlalchemy import Column, Boolean, Text, ForeignKey, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref, joinedload, lazyload
from app.shared.bases.base_model import ModelMixin, paginate, ModelType
from app.shared.schemas.ResponseSchemas import PagedBaseResponse, BaseResponse
from app.shared.schemas.page_schema import PagedResponse


class Agent(ModelMixin):
    __tablename__ = "agent"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    active = Column(Boolean)
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)
    accessToken = Column(String(255), nullable=True)
    quota = Column(Integer, default=0)
    adminId = Column(
        UUID(as_uuid=True),
        ForeignKey("admin.id", ondelete="CASCADE", link_to_name=True),
        index=True,
    )
    createdByAdmin = relationship(
        "Admin",
        foreign_keys="Agent.adminId",
        backref=backref("admin", single_parent=True),
    )

    @classmethod
    def agent_users(cls, agent_id: UUID, page_num: int, num_items: int):
        """
        It returns a paginated list of users for a given agent, with each
        user's credit account balance

        :param cls: The class of the model you're querying
        :param agent_id: UUID - The id of the agent
        :type agent_id: UUID
        :param page_num: The page number to return
        :type page_num: int
        :param num_items: number of items per page
        :type num_items: int
        :return: A paginated list of users
        """
        if user := cls.where(id=agent_id).join("users"):
            return paginate(user.users, page_num, num_items)
        # agent_user = cls.where(id=agent_id).options(
        #     joinedload(
        #         "users"
        #     ).options(
        #         joinedload(
        #             "creditAccount",
        #         ).load_only("balance")
        #         )
        #     )

        return   # paginate(users, page_num, num_items)

    @classmethod
    def add_agent(cls, *_, **kwargs) -> ModelType:
        """
        The add_agent function creates a new agent object.
        It takes in the following parameters:
            * _ - A list of objects that will be ignored by the function. These are usually objects passed into a function automatically, like HTTP request or database connections.
            * kwargs - Keyword arguments corresponding to fields in an agent object.

        :param cls: Used to Call the class itself.
        :param *_: Used to Catch any additional parameters that may be passed in.
        :param **kwargs: Used to Pass keyworded variable length of arguments to a function.
        :return: The agent instance.

        """
        agent_data = cls.rebuild(kwargs)
        if cls.where(email=agent_data["email"]).first():
            return
        agent = cls(**agent_data)
        cls.session.add(agent)
        cls.session.commit()
        return agent

    @classmethod
    def update_agent(cls, *_, **kwargs) -> ModelType:
        """
        The update_agent_user function updates the agent user with the given id.
        It takes in a dictionary of key value pairs to update and returns a dictionary of updated values.

        :param cls: Used to Refer to the class itself.
        :param *_: Used to Catch all the extra parameters that are passed in to the function.
        :param **kwargs: Used to Allow for any number of additional arguments to be passed into the function.
        :return: A dictionary of the updated agent user.

        """
        agent_user_id = kwargs.get("id")
        kwargs["updatedAt"] = datetime.datetime.now(pytz.utc)
        return cls.where(id=agent_user_id).update(**kwargs)

    @classmethod
    def remove_agent(cls, *_, **kwargs) -> UUID:
        """
        The remove_agent function removes the agent user with the given id.

        :param cls: Used to Refer to the class itself.
        :param *_: Used to Catch all the extra parameters that are passed in to the function.
        :param **kwargs: Used to Allow for any number of additional arguments to be passed into the function.
        :return: A dictionary of the updated agent user.

        """
        agent_user_id = kwargs.get("id")
        agent = cls.where(id=agent_user_id).delete()
        return agent.id

    @classmethod
    def list_all_agents(cls, page, num_items) -> PagedResponse:
        """
        The list_all_agent_users function returns a list of all agent users in the database.

        :param cls: Used to Refer to the class itself, rather than an instance of the class.
        :return: A dictionary of all the agent users in a class.
        """
        users = cls.session.query(
            cls.id,
            cls.email,
        )
        return paginate(users, page, num_items)

    @classmethod
    def get(cls, *_, **kwargs) -> ModelType:

        """
        returns an agent user with the given set of kwargs.

        :param self: Used to Refer to the class itself, rather than an instance of the class.
        :return: A dictionary of the user.
        """
        return cls.where(**kwargs).first()
