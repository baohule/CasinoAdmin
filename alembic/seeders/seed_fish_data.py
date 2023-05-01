import json
from json.decoder import NaN

from sqlalchemy import engine_from_config, MetaData, pool
from sqlalchemy.orm import Session

from app import logger
from app.api.game.models import Fish
import pandas as pd
import json

from app.endpoints.urls import APIPrefix


for route in APIPrefix.include:
    try:
        exec(f"from app.api.{route}.models import ModelMixin as Base")
    except ImportError as e:
        logger.error(f"Route {route} has no tables defined")

engine = engine_from_config(
    {"sqlalchemy.url": "postgresql+psycopg2://postgres:1121@localhost:5432/casino_admin"},
    prefix="sqlalchemy.",
    poolclass=pool.NullPool,
)
metadata = MetaData()
metadata.reflect(bind=engine)
session = Session(engine)


def generate_fish_config():
    df = pd.DataFrame({
        'fishType': range(30),
        'coin': [0, 0, 0, 0, 0, 2, 2, 3, 4, 5, 6, 7, 8, 9, 12, 10, 15, 18, 20, 25, 35, 40, 100, 30, 120, 300, 300, 200, 10, 300],
        'outPro': [0, 0, 0, 0, 5, 5, 8, 8, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 20, 15, 20, 15, 20, 15, 20, 20, 0, 0, 0, 0],
        'prop': [0] * 30,
        'propId': [0] * 30,
        'propCount': [0] * 30,
        'propValue': [0] * 30
    })
    df.loc[4:13, 'fishType'] += 10
    df.loc[14:17, 'fishType'] += 11
    df.loc[18:20, 'fishType'] += 14
    df.loc[21, 'fishType'] += 17
    df.loc[22:24, 'fishType'] += 20
    df.loc[25, 'fishType'] += 23
    df.loc[26, 'fishType'] += 2
    df.loc[27, 'fishType'] += 2
    df.loc[26:27, 'coin'] = 0
    df.loc[26, 'propId'] = 1
    df.loc[26, 'propCount'] = 1
    df.loc[26, 'propValue'] = 110
    df.loc[27, 'propId'] = 1
    df.loc[27, 'propCount'] = 10
    df.loc[27, 'propValue'] = 1100
    df.loc[28:32, 'fishType'] += 1
    df.loc[28:32, 'propId'] = 2
    df.loc[28:32, 'propCount'] = 1
    df.loc[28, 'propValue'] = 1
    df.loc[29, 'propValue'] = 3
    df.loc[30, 'propValue'] = 5
    df.loc[31, 'propValue'] = 8
    df.loc[32, 'propValue'] = 10
    df.columns = ['fishType', 'coin', 'outPro', 'prop', 'propId', 'propCount', 'propValue']
    return df.to_dict('records')



Fish.set_session(session)


fish_config = generate_fish_config()
Fish.seed_fish_config(fish_config)
fishes = Fish.where(fishType=NaN, coin=NaN).all()
[fish.delete() and fish.save() for fish in fishes]