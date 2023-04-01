"""
@author: Kuro
"""
import datetime
import pytz
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    JSON,
)

from app.api.game.schema import (
    CreateGameResponse,
)
from app.shared.bases.base_model import ModelMixin, paginate, ModelType
from app.shared.schemas.page_schema import PagedResponse


class GameList(ModelMixin):
    """
    GameList is a table that stores the game list.
    """

    __tablename__ = "game_list"

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
        game_data = cls.rebuild(kwargs)
        if cls.where(id=game_data["id"]).first():
            return CreateGameResponse(error="Game not Found")
        game = cls(**game_data)
        cls.session.add(game)
        cls.session.commit()
        return game

    @classmethod
    def update_game(cls, *_, **kwargs) -> ModelType:
        """
        > Update a game in the database

        :param cls: The class that the method is being called on
        :return: A class1 object with the success and response attributes.
        """
        game_id = kwargs.get("id")
        kwargs["updatedAt"] = datetime.datetime.now(pytz.utc)
        return cls.where(id=game_id).update(**kwargs)

    @classmethod
    def remove_game(cls, *_, **kwargs) -> ModelType:
        """
        It deletes a game from the database.

        :param cls: The class that the method is being called on
        :return: A BaseResponse object with the success and response attributes.
        """
        game_id = kwargs.get("id")
        return cls.where(id=game_id).delete()

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
