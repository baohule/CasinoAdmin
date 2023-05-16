"""
@author: Kuro
"""

import datetime
import uuid

import pytz
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    JSON, ForeignKey, Boolean, Float,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from app.api.game.schema import (
    CreateGameResponse,
)
from app.shared.bases.base_model import ModelMixin, paginate, ModelType
from app.shared.schemas.page_schema import PagedResponse


class GameList(ModelMixin):
    """
    GameList is a table that stores the game list.
    """

    __tablename__ = "GameList"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    eGameName = Column(String(255), nullable=False)
    cGameName = Column(String(255), nullable=False)
    type = Column(Integer)
    json = Column(JSON)
    createdAt = Column(DateTime)

    @classmethod
    def add_game(cls, *_, **kwargs) -> ModelType:
        """
        It creates a new game in the database.

        :param cls: The class that the method is being called on
        :return: CreateGameResponse
        """
        try:
            game_data = cls.rebuild(kwargs)
            if cls.where(id=game_data["id"]).first():
                return CreateGameResponse(error="Game not Found")
            game = cls(**game_data)
            cls.session.add(game)
            cls.session.commit()
            return game
        except Exception as e:
            cls.session.rollback()
            print(e)
            return


class GameSession(ModelMixin):
    """
    GameSession is a table that stores the game session.
    """
    __tablename__ = "GameSession"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True)
    gameId = Column(
        Integer,
        ForeignKey("GameList.id", ondelete="CASCADE", link_to_name=True),
        index=True,
        nullable=False,
    )
    game = relationship(
        "GameList",
        foreign_keys="GameSession.gameId",
        backref=backref("gameSession", single_parent=True, uselist=False)
    )

    createdAt = Column(DateTime, default=lambda: datetime.datetime.now(pytz.utc))
    updatedAt = Column(DateTime, nullable=True)



class PlayerSession(ModelMixin):
    """
    PlayerSession is a table that stores the player session.
    """
    __tablename__ = "PlayerSession"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4())
    gameSessionId = Column(
        UUID(as_uuid=True),
        ForeignKey("GameSession.id", ondelete="CASCADE", link_to_name=True),
        index=True,
        nullable=True,
    )
    gameSession = relationship(
        "GameSession",
        foreign_keys="PlayerSession.gameSessionId",
        backref=backref("gameSession", single_parent=True),
    )
    userId = Column(
        Integer,
        ForeignKey("User.id", ondelete="CASCADE", link_to_name=True),
        index=True,
        nullable=False,
    )
    user = relationship(
        "User",
        foreign_keys="PlayerSession.userId",
        backref=backref("userSessions", single_parent=True),
    )
    betAmount = Column(Integer, nullable=False)
    betLines = Column(Integer, nullable=True)
    betResult = Column(Integer, nullable=True)
    createdAt = Column(DateTime, default=lambda: datetime.datetime.now(pytz.utc))

    @classmethod
    def update_game(cls, *_, **kwargs) -> ModelType:
        """
        > Update a game in the database

        :param cls: The class that the method is being called on
        :return: A class1 object with the success and response attributes.
        """
        try:
            game_id = kwargs.get("id")
            kwargs["updatedAt"] = datetime.datetime.now(pytz.utc)
            update = cls.where(id=game_id).update(**kwargs)
            cls.session.commit()
            return update
        except Exception as e:
            cls.session.rollback()
            print(e)
            return

    @classmethod
    def remove_game(cls, *_, **kwargs) -> ModelType:
        """
        It deletes a game from the database.

        :param cls: The class that the method is being called on
        :return: A BaseResponse object with the success and response attributes.
        """
        try:
            game_id = kwargs.get("id")
            return cls.where(id=game_id).delete()
        except Exception as e:
            cls.session.rollback()
            print(e)
            return

    @classmethod
    def list_all_games(cls, page, num_items) -> PagedResponse:
        """
        > This function returns a list of all games in the database, sorted by name, in reverse order

        :param cls: The class that the method is being called on
        :param page: The page number to return
        :param num_items: The number of items to return per page
        :return: A PagedBaseResponse object
        """
        games = cls.where()
        games_pages: PagedResponse = paginate(games, page, num_items)
        games_pages.items = sorted(
            games_pages.items, key=lambda x: x.name, reverse=True
        )
        return games_pages

    @classmethod
    def get(cls, *_, **kwargs) -> ModelType:
        """
        "Get the first instance of a class that matches the given keyword arguments."

        The first line of the function is a docstring. It's a string that describes what the function does. It's good practice to include a docstring for every function you write

        :param cls: The class that the method is being called on
        :return: The first instance of the class that matches the query.
        """
        return cls.where(**kwargs).first()


class Fish(ModelMixin):
    __tablename__ = 'fish'

    id = Column(Integer, primary_key=True)
    fishType = Column(Float)
    coin = Column(Float)
    outPro = Column(Float)
    prop = Column(Float)
    propId = Column(Float)
    propCount = Column(Float)
    propValue = Column(Float)  # Only for certain fish types

    @classmethod
    def seed_fish_config(cls, fish_config):
        for config in fish_config:
            fish = cls(**config)
            cls.session.add(fish)
        cls.session.commit()


class Paths(ModelMixin):
    __tablename__ = 'paths'

    id = Column(Integer, primary_key=True)
    duration = Column(DateTime)
    starting = Column(Float)
    middle = Column(Float)
    destination = Column(Float)
