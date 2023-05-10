"""
@author: igor
"""
from app import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from socketio import asyncio_server as AsyncServer
from app.rpc.user.schema import Game
from app.rpc.user.schema import BaseUser
from app.rpc import socket


@socket.on('LoginGame')
def log_in_game(data: Game):
    # sio.emit('LoginGameResult')
    return


@socket.on('getCoinRank')
def get_coin_rank(data: BaseUser, context):
    # sio.emit('getCoinRankResult')
    return


@socket.on('updateNickName')
def update_nick_name(data: BaseUser):
    # sio.emit('updateNickNameResult')
    return


@socket.on('updateHeadUrl')
def update_head_url(data: BaseUser):
    # sio.emit('updateHeadUrlResult')
    return
