"""
@author: Kuro
"""
from starlette.requests import Request

from app.api.credit.models import Balance
from app.api.user.models import User
from app.rpc import socket
from app.rpc.user.schema import BaseUser


class RPCUserRoutes:

    @socket.on("getUserCredit")
    def get_user_credit(self, request: Request):
        """
        The get_user_credit function is used to get the credit balance of a user.
            Args:
                context (BaseUser): The user who's credit balance we want to retrieve.
                request (Request): The request object that was sent from the client side.

        Args:
            self: Represent the instance of a class
            context: BaseUser: Get the user's id
            request: Request: Get the request object

        Returns:
            The balance of the user

        """
        balance = Balance.read(ownerId=request.user.id)
        socket.emit('getUserCreditResult', balance)
        return

    @socket.on("getCoinRank")
    def get_coin_rank(self):
        """
        The get_coin_rank function is used to get the top 10 users with the most coins.
        It does this by querying for all users who have a balance greater than 0, and then ordering them by their balance in descending order.
        The function then limits the results to only return 10 of these users, and returns them as a list.

        Args:

        Returns:
            The top 10 users with the most coins
        """
        coin_rank = User.where(balance___amount__gt=0).order_by(
            User.balance___amount.desc()
        ).limit(10).all()
        socket.emit('getCoinRankResult', coin_rank)
        return

    @socket.on("updateNickName")
    def update_nick_name(self, context: BaseUser, request: Request):
        """
        The update_nick_name function is used to update the username of a user.
            It takes in a BaseUser object and uses it's username property to update the User model.
            The updated user is then sent back through socketio.

        Args:
            context: BaseUser: Pass the user object to the function
            request: Request: Get the user's id from the request

        Returns:
            Nothing
        """
        user = User.read(id=request.user.id)
        user.username = context.username
        user.save()
        socket.emit('updateNickNameResult', user)
        return

    @socket.on("updateHeadUrl")
    def update_head_url(self, context: BaseUser, request: Request):
        """
        The update_head_url function updates the headImage field of a user in the database.

        Args:
            context: BaseUser: Get the head image from the client
            request: Request: Get the user's id

        Returns:
            The user's head image url
        """
        user = User.read(id=request.user.id)
        user.headImage = context.headImage
        user.save()
        socket.emit('updateHeadUrlResult', user)
        return
