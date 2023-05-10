# let schedule = require("node-schedule");
# let Fish = require("./Fish");
# let gameConfig = require("./../config/gameConfig");
#
# let fishConfig;
# let log = require("./../../../CClass/class/loginfo").getInstand;
# let fishOutListConfig = require("./../config/fishOutListConfig");
#
# let redis_send_and_listen = require("./../../../util/redis_send_and_listen");
import itertools
import random
import time
from typing import List, Optional, Dict, Any

import numpy as np
import schedule
from collections import defaultdict
from datetime import datetime
import pydantic
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_socketio import SocketManager
from py_linq import Enumerable
from socketio import asyncio_server as AsyncServer
from typing import List, Union
from pydantic import BaseModel, Field, validator
import pandas as pd
from socketio.asyncio_namespace import AsyncNamespace
from starlette.websockets import WebSocket

from app.api.game.models import Fish
from app import logging
from app.rpc.game_server import User

logger = logging.getLogger("fish_game")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
sio = AsyncServer(async_mode="asgi", cors_allowed_origins="*")
sio.attach(app)

fishConfig = Fish.where().all()


class FishConfig(BaseModel):
    """
    The FishConfig class is a Pydantic model that represents
    a fish configuration. It contains the following attributes:
    """
    coin: int
    propValue: int
    outPro: int
    outProMax: int
    outProMin: int
    outProMaxTime: int
    outProMinTime: int


class GameConfig(BaseModel):
    """
    The GameConfig class is a Pydantic model that represents
    a game configuration. It contains the following attributes:
    """
    controlBet: int
    serverId: str


class Fish(BaseModel):
    """
    The Fish class is a Pydantic model that represents a
    fish in the game. It contains the following attributes:
    """
    fish_id: int
    fish_type: int
    fish_path: str
    coin: int
    fish_count: int


class FishOut(BaseModel):
    """
    The FishOut class is a Pydantic model that represents
    a fish out event in the game. It contains the following attributes:
    """
    fishOutList: List[int] = []
    fishOutProMax: int = 0

    class LoginParams(User):
        userlist: Optional[dict]

    class LoginResponse(BaseModel):
        tableId: int
        seatId: int

    class Room(BaseModel):
        roomid: Optional[str]
        onlienPepole: int = 0
        tableMax: int = 10
        seatMax: int = 4
        tableList: List[List[AsyncServer]] = Field(default_factory=lambda: [[None] * 5] * 10)


class FishGame:
    """
    The FishGame class is a Pydantic model that represents
    an instance of a fish game or fish game like application.
    """

    MAX_SEATS = 4
    MAX_TABLES = 500
    MAX_FISH_COUNT = 10000

    def __init__(self):
        self.seatMax = self.MAX_SEATS
        self.tableList = defaultdict(lambda: [None] * (self.seatMax + 1))
        self.onlinePeople = 0
        self.roomId = 0
        self.fish_id = 0
        self.fishList = defaultdict(dict)
        self.delFishList = []
        self.changeSceneType = 0
        self.changeFishOutI = 0
        self.isSendingChange = False
        self.changeingFishScene = False
        self.del_fish_list = None
        self.fish_list: Dict[str, Dict[int, Fish]] = {}

    def init(self):
        """
        The function "init" initializes the fish game by calling the
        "init_bet_arr"function and logger.infoing a message to the console.
        """
        rule = sio.enter_background_task(self.schedule_fish_out)

        self.init_bet_arr()
        logger.info("FishGame init")

    async def schedule_fish_out(self):
        """
        This is an asynchronous function that schedules
        a job to run every second, which updates the fish
        scene and emits information about fish caught to a socket.
        """
        times = range(0, 60)
        rule = {"second": times}

        # TODO: Add a table_string, AND
        #  info parameters to the fish_scene_job function
        async def fish_scene_job(table_string=None, info=None):
            now = datetime.now()
            hour, minute, second = now.hour, now.minute, now.second

            if minute % 20 == 0 and not second:
                self.changeingFishScene = True
                self.isSendingChange = True
                self.changeSceneType += 1
                self.changeSceneType %= 3
                self.changeFishOutI = 0
            if self.changeingFishScene:
                self.change_fish_out()
            else:
                fish_info = self.fish_out()

                # Create a list of fish_infos to process
                fish_infos = [fish_info]
                if second % 2:
                    fish_info1 = self.fish_out()
                    fish_infos.append(fish_info1)

                # Use the intersect method from py_linq to get the common unique fish_ids from all fish_infos
                fish_ids = Enumerable(fish_infos[0].fish_id).intersect(
                    *[Enumerable(info.fish_id) for info in fish_infos[1:]])

                # Update the fishList with the common unique fish_ids
                for index, fish_id in enumerate(fish_ids):
                    self.fishList[index].update({
                        fish_id: self.pop_or_create_fish(fish_id, fish_info.fish_type, fish_info.fish_path,
                                                         fish_info.coin)
                    })
                    await sio.emit('FishOut', info.dict(), room=table_string)

        schedule.every(1).seconds.do(fish_scene_job)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def pop_or_create_fish(self, fish_id: int, fish_type: int, fish_path: str, coin: int):
        """
        This function either pops a fish from a list or creates a new fish object with given parameters.

        :param fish_id: The unique identifier for the fish object being created or retrieved
        :param fish_type: The type of fish being created or popped from the list. It could be a string or an integer value that represents the type of fish. For example, it could be
        "salmon", "tuna", "shark", or 1, 2, 3, etc. depending on
        :param fish_path: fish_path is a string parameter that represents the path or location of the fish image file. It is used to load the image of the fish and display it on the
        screen
        :param coin: The "coin" parameter is likely a variable that represents the value or amount of currency associated with the fish object being created or retrieved. It could be
        used to determine the cost of the fish, the amount of money earned by catching the fish, or other financial calculations related to the game or application that
        :return: an instance of the `Fish` class with the specified `fish_id`, `fish_type`, `fish_path`, and `coin` values. If there are any previously deleted fish objects in the
        `delFishList`, the function will return the last deleted fish object after re-initializing it with the specified values. Otherwise, a new `Fish` object will be created with the
        """
        if self.delFishList:
            fish = self.delFishList.pop()
            fish.init(fish_id, fish_type, fish_path, coin)
        else:
            fish = Fish(
                fish_id=fish_id,
                fish_type=fish_type,
                fish_path=fish_path,
                coin=coin
            )
        return fish

    def fish_out(self):
        """
        The function "fish_out" is a placeholder that logger.infos a message and returns an empty Fish object.
        :return: An instance of the `Fish` class created using `pydantic.parse_obj_as()` with an empty dictionary as the input.
        """
        logger.info("FishOut function called")
        return pydantic.parse_obj_as(Fish, {})

    def change_fish_out(self):
        """
        The function "change_fish_out" is defined but has no code inside it.
        """
        logger.info("change_fish_out function called")

    def init_bet_arr(self):
        """
        The function "init_bet_arr" is defined but has no code inside it.
        """
        logger.info("init_bet_arr function called")


class ProCount(BaseModel):
    """
    The ProCount class is a class that represents a pro count.
    """
    pro_count: List[List[List[int]]] = Field(default_factory=list)


class BetArr(BaseModel):
    """
    The BetArr class is a class that represents a bet array.
    """
    pro_count: ProCount = Field(default_factory=ProCount)
    hit_times: List[List[int]] = Field(default_factory=list)
    prop_fish_hit_count: List[int] = Field(default_factory=list)


class LoginResponse(BaseModel):
    """
    The LoginResponse class is a class that
    represents a response to a login request.
    """

    tableId: int
    seatId: int


# initialize tableList
table_list = [[None] * 9 for _ in range(3)]
table_list[0][-1] = 0
table_list[1][-1] = 0
table_list[2][-1] = 0


class ClickOdd(BaseModel):
    click: int
    percent: int
    cycle: int
    minpool: int
    maxpool: int


class Player(BaseModel):
    username: str
    table_id: int
    seat_id: int


class Pool(BaseModel):
    pool: int


class User(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.table_id = None

    id: str
    tableId: int
    _Robot: Optional[bool] = False


class FishInfo(BaseModel):
    fish_id: int
    hitInfo: str


class GameInfo(BaseModel):
    totalwin: int
    totalbet: int
    gametype: int


class FishNameSpace(AsyncNamespace):
    pool: float = 0
    betCount: List[int] = [1, 5, 10, 20, 30, 50, 100]
    fishList: dict = {}
    virtualPool: float = 0


class GameConfig(BaseModel):
    clickodd: List[ClickOdd]


game_config = GameConfig(clickodd=[
    {'click': 10, 'percent': 5, 'cycle': 2, 'minpool': 1, 'maxpool': 10},
    {'click': 20, 'percent': 10, 'cycle': 3, 'minpool': 2, 'maxpool': 20},
    {'click': 50, 'percent': 20, 'cycle': 4, 'minpool': 5, 'maxpool': 50},
    {'click': 100, 'percent': 30, 'cycle': 5, 'minpool': 10, 'maxpool': 100},
    {'click': 200, 'percent': 50, 'cycle': 6, 'minpool': 15, 'maxpool': 200},
    {'percent': 80, 'cycle': 7, 'minpool': 20, 'maxpool': 300}
])


class CurrentUser(BaseModel):
    playerclick: int


pro_max = [10, 20, 30]
bet_count = [1, 2, 3]
pro = [0.2, 0.3, 0.4]


class FishNamespace(FishGame):
    def delete_fish(self, table_obj: Dict[int, Fish], fish_id: int) -> None:
        fish = table_obj.get(fish_id)
        if fish:
            fish.deleted = True
            self.del_fish_list.append(fish)
            del table_obj[fish_id]

    @validator("fish_id")
    def validate_fish_id(cls, v):
        if not isinstance(v, int):
            raise ValueError("fish_id must be an integer")
        elif v < 0:
            raise ValueError("fish_id must be non-negative")
        return v

    @validator("fish_type")
    def validate_fish_type(cls, v):
        if not isinstance(v, int):
            raise ValueError("fish_type must be an integer")
        elif v < 0 or v >= len(fishConfig):
            raise ValueError(f"fish_type {v} out of range")
        return v


class HitTimes:
    pass


class PoolInfo(BaseModel):
    pool: int
    virtualPool: int


class SkillInfo(BaseModel):
    sid: int


class Boom:
    pass


class FishServer(FishGame):
    """
The FishServer class is a class that represents a
server for the FishGame class. It is used to create a
FishGame object and run the game.
    """
    def __init__(self, fish_config: List[FishConfig], game_config: GameConfig, socket_str: str):
        super().__init__()
        self.fishOut = None
        self.max_pool = None
        self.betCount = None
        self.tableList = None
        self.tableMax = None
        self.seatMax = None
        self.onlienPepole = None
        self.fish_config = fish_config
        self.game_config = game_config
        self.socket_str = socket_str
        self.pro = []
        self.prop = []

        self.fish_out_time = [0] * len(self.fish_config)
        for i, fc in enumerate(self.fish_config):
            if fc.coin > 0:
                self.pro.append(fc.coin)
            else:
                self.prop.append(fc.propValue)

        self.prop_id = [0, 0]
        self.prop_count = [1, 10]
        self.bet_count = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 2, 2.5, 3, 3.5, 4, 4.5, 5]

        self.control_pool = {'line': 0, 'pool': 0}
        self.pro_max_count = []
        self.pro_max = []
        self._fish_out_pro_max = 0
        self._fish_out_other_type = -1
        self._fish_out_other_path = -1
        self._fish_out_other_count = 0
        self._prop_fish_hit_count = {}
        self.is_send_end_msg = False
        self.match_id = 0
        self.match_login = True
        self.is_send_prize = False
        self.clean_rank = False
        self.apply_flag = True
        self.last_path = 0
        self.changing_fish_scene = False
        self.is_send_change = False
        self.change_type = 0
        self.change_scene_type = 0
        self.change_fish_out_i = 0
        self.boom_list = []
        self.moguiyue_user_list = {}
        self.moguiyue_out_list = [0.2, 0.4, 0.6, 0.8, 3.2]
        self.pool = 0
        self._test_max = 0
        self.cleanRank = False
        self.fish_config = []
        self.pro_count = []
        self.hit_times = []
        self.prop_fish_hit_count = [0, 0, 0]
        self.io = None  # initialize to None
        self.c_socket = None  # initialize to None
        self.last_path = 0
        self.fish_id = 0
        self.fish_count_max = 10000000  # assuming some large number
        self.fish_count = 0
        self.fish_out_list = []
        self.last_path = 0
        self.fish_out_pro_max = 0
        self.moguiyueUserList: Dict[int, Dict[str, int]] = {}
        self.pool: int = 0
        self.virtualPool: int = 0
        self.skill_cost: list[int] = [10, 20]
        self.reward_pool: int = 0
        self.bullet_pool = []

        self.init_fish_out_pro()

    def set_catch_chance(self, info):
        """
        The function "set_catch_chance" takes in an argument "info" but does not have any code implemented yet.

        :param info: It is unclear what the "info" parameter is supposed to represent without more context. It could be any type of information related to setting the catch chance,
        such as a percentage value or a list of factors that affect the chance
        """
        pass

    def change_pool(self, num):
        """
        This function updates the control pool value and sets it in the game configuration.

        :param num: The parameter "num" is an integer value that represents the amount by which the "pool" value in the "control_pool" dictionary needs to be changed. The function adds
        this value to the current "pool" value and updates the "control_pool" dictionary with the new value
        """

        self.control_pool['pool'] += num
        self.set_control_pool({'serverId': self.game_config.serverId, 'pool': self.control_pool['pool']})

    def set_control_pool(self, info):
        """
        This is an empty function that sets the control pool with the given information.

        :param info: The "info" parameter is likely a variable or object that contains information related to setting a control pool. Without more context, it's difficult to determine
        exactly what kind of information it might contain
        """
        pass

    def set_control_line(self, info):
        """
        This is an empty function that sets a control line with the given information.

        :param info: The "info" parameter is likely a dictionary or object containing information about a control line. Without more context, it's difficult to say exactly what
        information is expected to be included in this parameter. The function itself doesn't do anything with the information passed in, as it simply contains a "pass"
        """
        pass

    def get_control_pool(self):
        """
        The function initializes a dictionary called "control_pool" with two keys, "line" and "pool", both with a value of 0.
        """
        self.control_pool = {'line': 0, 'pool': 0}

    def get_clean_rank(self) -> bool:
        """
        This function returns the clean rank of an object.
        :return: A boolean value representing the clean rank.
        """
        return self.cleanRank

    def open_clean_rank(self):
        """
        This function sets the "cleanRank" attribute to True.
        """
        self.cleanRank = True

    def off_clean_rank(self):
        """
        This function sets the "cleanRank" attribute to False.
        """
        self.cleanRank = False

    def init_fish_out_pro(self):
        """
        The function initializes a fish_out_pro attribute and a FishOut object using a fish_config dataframe and a generated fish_out_list.
        """
        fish_config_data = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13]]
        self.fish_config = pd.DataFrame(fish_config_data, columns=["outPro"], index=range(1, 14))
        self.fishOut = FishOut(fishOutList=self.generate_fish_out_list(),
                               fishOutProMax=self.fish_config["outPro"].cumsum().max())

    def generate_fish_out_list(self) -> List[int]:
        """
        This function generates a list of integers representing fish types based on their probability of being caught.
        :return: a list of integers representing the fish that can be caught in a fishing game. The list is generated based on the probabilities of each fish being caught, which are
        stored in a pandas DataFrame called "fish_config". The function loops through the DataFrame and adds each fish to the list a number of times equal to its "outPro" value.
        """
        fish_out_list = []
        for i in range(13):
            fish_out_list += [i] * self.fish_config.iloc[i + 1]["outPro"]
        return fish_out_list

    def init_bet_arr(self, pro: List[int], bet_count: List[int], control_bet: float) -> None:
        """
        This function initializes a betting array based on given parameters and uses random number generation to populate the array.

        :param pro: A list of probabilities for each fish to be caught
        :type pro: List[int]
        :param bet_count: `bet_count` is a list of integers representing the different bet amounts that can be placed
        :type bet_count: List[int]
        :param control_bet: `control_bet` is a float variable that represents the maximum bet amount that can be placed on a particular outcome. It is used in the function to calculate
        the maximum count of a particular outcome based on its probability
        :type control_bet: float
        """
        self.prop_fish_hit_count = [0] * len(pro)
        for i in range(len(pro)):
            self.pro_count.append([])
            self.hit_times.append([])
            max_count = int(10000 / pro[i])
            self.pro_max_count = int(max_count * control_bet)
            self.pro_max = self.pro_max_count * pro[i]

            for j in range(len(bet_count)):
                self.pro_count[i].append([0] * 9999)
                self.hit_times[i].append(0)
                point = 0
                for _ in range(self.pro_max_count):
                    point += np.random.randint(low=0, high=pro[i])
                    self.pro_count[i][j][point] = 1
                    point += 1

                for _, k in itertools.product(range(10), range(5000)):
                    temp = self.pro_count[i][j][k]
                    idx = np.random.randint(low=0, high=self.pro_max)
                    self.pro_count[i][j][k] = self.pro_count[i][j][idx]
                    self.pro_count[i][j][idx] = temp

        for i in range(len(self.prop_fish_hit_count)):
            self.reset_prop(i)

    def reset_prop(self, idx: int) -> None:
        """
        This function resets a property of an object by generating a random integer within a certain range based on the original value of the property.

        :param idx: idx is an integer parameter representing the index of a specific property in a list or array
        :type idx: int
        """
        offset = int(self.prop[idx] * 0.2)
        self.prop_fish_hit_count[idx] = np.random.randint(low=offset, high=(self.prop[idx] * 2))

    def set_io(self, io: SocketManager, socket_classname: str) -> None:
        """
        This function sets the input/output and socket class for a given object.

        :param io: io is a parameter of type SocketManager, which is likely a class that manages sockets for network communication. It is used to set the io attribute of the current
        object to the provided io parameter
        :type io: SocketManager
        :param socket_classname: The parameter `socket_classname` is a string that represents the name of a socket class. It is used to specify the type of socket that will be used for
        communication
        :type socket_classname: str
        """
        self.io = io
        self.c_socket = socket_classname

    async def get_fish_path(self) -> str:
        """
        This function returns the path to a fish image.
        :return: A string representing the path to a fish image.
        """
        fish_id = np.random.randint(1, 10)
        return f'/static/fish{fish_id}.png'

    @sio.on('fish_out')
    async def fish_out(self):
        """
        The function `fish_out` selects a type of fish to be
        caught based on probability and time constraints, while the
        function `LoginRoom` assigns a user to an available seat in a
        game room.
        :return: The `select_fish_type` function is being returned.
        """

        fish_configs = {i: Fish(**x) for i, x in enumerate(Fish.where().all())}
        fish_out_list = list(fish_configs.keys())

        fish_out_time = [0] * len(fish_configs)

        def _select_fish_type(fish_out_list, fish_configs, fish_out_time, fish_out_pro_max):
            """
            This function selects a fish type based on probability and time constraints.

            :param fish_out_list: A list of integers representing the types of fish that can be caught
            :param fish_configs: A dictionary containing configurations for different types of fish. Each key represents a fish type and the corresponding value is an object containing
            various properties such as the fish's name, image, rarity, and probability of being caught
            :param fish_out_time: A list containing the remaining time (in seconds) until each fish type can be selected again for fishing
            :param fish_out_pro_max: fish_out_pro_max is the maximum probability value for selecting a fish type from the list of available fish types. It is used in the random number
            generation to determine which fish type to select
            """
            fish_type_pro = random.randint(0, fish_out_pro_max - 1)

            if fish_type_pro > ((2 / 3) * fish_out_pro_max) and fish_configs[25].outPro:
                fish_type = 25
            elif fish_type_pro > ((1 / 3) * fish_out_pro_max) and fish_configs[24].outPro:
                fish_type = 24
            else:
                fish_type = fish_out_list[fish_type_pro]

            for i, fish in enumerate(fish_configs.values()):
                if fish.outPro:
                    if fish_out_time[i] <= 0:
                        fish_type = i
                        fish_out_time[i] = fish.outPro
                        break
                    fish_out_time[i] -= 1

            return fish_type

        return _select_fish_type(fish_out_list, fish_configs, fish_out_time, self.fish_out_pro_max)

    def getTablePlayers(self, tableidx: int):
        """
        This function returns a list of players seated at a specific table index.

        :param tableidx: The parameter `tableidx` is an integer representing the index of the table in the `tableList` attribute of the object. The function `getTablePlayers`
        returns a list of integers representing the indices of the players who are currently seated at the table with the given index. The function uses a list
        :type tableidx: int
        :return: The function `getTablePlayers` is returning a list of integers representing the player indices who are currently seated at the table with the index `tableidx`. The
        list comprehension `[i for i in range(self.seatMax) if self.tableList[tableidx][i]]` creates a list of all the indices `i` from 0 to `self.seatMax` where
        `self.tableList[table
        """
        return [i for i in range(self.seatMax) if self.tableList[tableidx][i]]

    async def LoginRoom(self, user: User, socket: AsyncServer, userlist: Optional[dict]) -> LoginResponse:
        """
        This function allows a user to login to a room by finding an available seat and adding their socket to the corresponding table.

        :param user: The user object represents the user who is trying to login to the room
        :type user: User
        :param socket: AsyncServer is an object representing a WebSocket connection. It is used to send and receive messages between the client and server asynchronously
        :type socket: AsyncServer
        :param userlist: userlist is a dictionary that contains information about the user and the room they are trying to join. It may include the RoomId, which is the unique
        identifier for the room. This parameter is optional and may be None
        :type userlist: Optional[dict]
        :return: A LoginResponse object is being returned, which contains the tableId and seatId of the user who has successfully logged into the room. If the room is full, the tableId
        and seatId will both be -1.
        """
        if self.onlienPepole > self.tableMax * self.seatMax:
            logger.info("The number of people in the room is full")
            return LoginResponse(tableId=-1, seatId=-1)

        self.onlienPepole += 1
        tableidx = -1
        seatidx = -1
        nullseat = False
        self.roomid = userlist.get('RoomId', None) if userlist else None

        for table_index, table in enumerate(self.tableList):
            nullseat = False
            for seat_index, seat in enumerate(table):
                if not seat:
                    nullseat = True
                    tableidx, seatidx = table_index, seat_index
                    break
            if nullseat:
                break

        if tableidx == -1 or seatidx == -1:
            logger.info("The room is full")
            return LoginResponse(tableId=-1, seatId=-1)

        self.tableList[tableidx][seatidx] = socket
        self.tableList[tableidx][self.seatMax] = 1

        tablestring = "table" + str(tableidx)
        await socket.join_room(tablestring)

        return LoginResponse(tableId=tableidx, seatId=seatidx)

    # room = Room()
    #
    # @app.post("/loginroom", response_model=LoginResponse)
    # async def loginroom(params: LoginParams):
    #     return await room.LoginRoom(params, server, params.userlist)

    def get_table_players(table_id: int) -> List[Union[Player, None]]:
        """
        The function returns a list of players seated at a specified table, or None if the seat is empty.

        :param table_id: an integer representing the ID of the table for which we want to retrieve the list of players
        :type table_id: int
        :return: The function `get_table_players` is returning a list of players (or `None` values) who are currently seated at the table with the given `table_id`. The function is
        using a list comprehension to iterate over the seats at the table and filter out any `None` values, returning only the seats that have a player seated in them.
        """
        return [seat for seat in table_list[table_id] if seat is not None]

    def logout_room(user: Player, socketio_sid: str) -> None:
        """
        The function logs out a player from a table and removes them from the corresponding room in a SocketIO server.

        :param user: The user parameter is an instance of the Player class, which represents a player in the game. It contains information about the player's table ID, seat ID, and
        other attributes
        :type user: Player
        :param socketio_sid: The `socketio_sid` parameter is a string that represents the unique identifier of a Socket.IO connection. It is used to identify the specific client
        connection that is being logged out of a room
        :type socketio_sid: str
        :return: None.
        """
        table_id, seat_id = user.table_id, user.seat_id
        if table_id == -1 or seat_id == -1:
            return

        if table_list[table_id]:
            table_list[table_id][seat_id] = None

        is_online = any([seat for seat in table_list[table_id]])
        if not is_online:
            table_list[table_id][-1] = 0

        room_str = f"table{table_id}"
        sio.leave_room(socketio_sid, room_str)

    def send_pool(pool: Pool) -> None:
        """
        The function sends a pool object to a specific room using Socket.IO.

        :param pool: The parameter `pool` is of type `Pool`. It is likely an object that contains information about a pool of resources or data that needs to be sent to a client or
        server. The `.dict()` method suggests that it may be a dictionary-like object
        :type pool: Pool
        """
        for i, table in enumerate(table_list):
            if table[-1] is not None:
                room_str = f"table{i}"
                sio.emit("pool", pool.dict(), room=room_str)

    async def on_connect(self, sid: str, environ: dict):
        """
        This is an asynchronous function that emits a 'init' event with a dictionary containing a 'pool' key and its corresponding value to the socket identified by the given sid.

        :param sid: `sid` stands for "session ID". It is a unique identifier assigned to each client that connects to the server using Socket.IO. The server uses this ID to keep track
        of the client's connection and to send messages to that specific client
        :type sid: str
        :param environ: The `environ` parameter is a dictionary containing the environment variables of the current request. These variables can include information such as the request
        method, headers, and other metadata. In the context of a Socket.IO server, the `environ` dictionary may also contain information about the client's connection,
        :type environ: dict
        """
        await sio.emit('init', {'pool': self.pool})

    async def shooting(self, data: dict):
        user = User(**data['user'])


    async def on_fish_hit(self, sid: str, data: dict):
        """
        This is a function that handles the logic for when a fish is hit in a game, calculating the score and updating various game and user information.

        :param sid: The parameter `sid` is a string representing the session ID
        :type sid: str
        :param data: The `data` parameter is a dictionary containing information about the fish hit event. It includes the user's information (`'user'`), the bet amount (`'bet'`),
        information about the fish that was hit (`'fish'`), and information about the game (`'gameinfo'
        :type data: dict
        :return: A dictionary with keys 'score', 'propId', and 'propCount' and their respective values.
        """
        user = User(**data['user'])
        bet = int(data['bet'])
        fish_data = FishInfo(**data['fish'])
        fish_id = fish_data.fish_id

        target_fish = self.fishList[user.table_id][fish_id].getfish_type()
        is_kill = self.compute_probability(fish_data.fish_type)
        if target_fish < 0 or target_fish >= len(fishConfig) \
                or bet not in self.betCount \
                or not self.fishList[user.table_id].get(fish_id) \
                or self.fishList[user.table_id][fish_id].getfish_id() != fish_id \
                or self.fishList[user.table_id][fish_id].isDel()\
                or not is_kill:
            return {'score': 0, 'propId': 0, 'propCount': 0}
        return {'userId': user.id, 'score': fish_data.coin, 'fish_id': fish_id, 'propId': 0, 'propCount': 0}

    def compute_probability(self, fish_type: int):
        seed: float = random.random()
        difficulty_level: int = self.fishConfig[fish_type].difficulty
        prob_range: list = [(difficulty_level - 1) * 0.05, difficulty_level * 0.05]
        if prob_range[0] <= seed < prob_range[1]:
            return True
        return False


    async def boom_fish_hit(self, user: User, bet: float, hit_count: int, fish_id: int, boom_level: int):
        """
        This function checks if a given bet, fish, and boom level are valid and initializes certain variables if they are not.

        :param user: The user parameter is an instance of the User class, which likely contains information about the player making the bet and playing the game
        :type user: User
        :param bet: A float value representing the amount of bet placed by the user
        :type bet: float
        :param hit_count: The parameter `hit_count` is an integer that represents the number of times the fish has been hit
        :type hit_count: int
        :param fish_id: The ID of the fish that was hit
        :type fish_id: int
        :param boom_level: The boom_level parameter is an integer that represents the level of the boom used to hit the fish. It is used in the function to determine the probability of
        hitting the fish and calculating the score
        :type boom_level: int
        :return: A dictionary with a key "score" and a value of 0.
        """
        if bet not in self.bet_count:
            logger.info("")
            return {"score": 0}

        table_obj = self.fish_list.get(user.table_id)
        if not table_obj or fish_id not in table_obj:
            logger.info("")
            return {"score": 0}

        fish = table_obj[fish_id]
        if fish.fish_id != fish_id or fish.deleted:
            logger.info("")
            return {"score": 0}

        fish_type = fish.fish_type
        if fishConfig[fish_type]:
            logger.info(f"{fishConfig[fish_type].prop}")
            return {"score": 0}

        if fish_type == 23 or fish_type == 25 or fish_type == 21 or fish_type >= 28:
            logger.info("")

            self.pro_max = pro_max
            self.pro = pro
            n_pro = len(pro_max)
            n_bet = len(self.betCount)
            self.hit_times = HitTimes(values=[[0] * n_bet for _ in range(n_pro)])
            self.pro_count = ProCount(pro_count=[[[i] * n_bet for j in range(1000)] for i in range(n_pro)])
            self.boom_list = []

            return {"score": 0}

    def delete_fish(self, table_obj: Any, fish_id: int, reason: str) -> None:
        """
        The function `delete_fish` takes a table object, a fish ID, and a reason as input and deletes the corresponding fish from the table.

        :param table_obj: The table object is likely an instance of a class representing a database table. It is being passed as an argument to the method so that the method can
        interact with the table and delete a specific fish record from it
        :type table_obj: Any
        :param fish_id: The fish_id parameter is an integer that represents the unique identifier of the fish that needs to be deleted from the table
        :type fish_id: int
        :param reason: The "reason" parameter is a string that represents the reason for deleting a fish from a table. It could be anything from the fish being spoiled or expired, to
        the customer changing their mind about the order. The specific reason will depend on the context in which this method is being used
        :type reason: str
        """
        pass  # implementation omitted

    def get_score(self, pro: int, betidx: int, hit_count: int, fish_id: int, table_obj=None, boom_level=None) -> float:
        """
        This function calculates the score for a given bet and hit count, and deletes a fish from a table if the score is greater than zero.

        :param pro: pro is an integer parameter representing the probability level of a certain event happening
        :type pro: int
        :param betidx: betidx is an integer parameter representing the index of the bet being placed
        :type betidx: int
        :param hit_count: The number of times the player hit the fish with their weapon
        :type hit_count: int
        :param fish_id: The parameter fish_id represents the unique identifier of the fish that was hit
        :type fish_id: int
        :param table_obj: The table object is a variable that represents the current state of the game table. It is not used in this function, but it may be used in other parts of the
        code
        :return: a float value, which is either the score earned by the player or 0.
        """
        if (hit_count // 10) >= self.pro_max[pro]:
            for k in range(1000):
                temp = self.pro_count.values[pro][betidx][k]
                idx = np.random.randint(self.pro_max[pro])
                self.pro_count.values[pro][betidx][k] = self.pro_count.values[pro][betidx][idx]
                self.pro_count.values[pro][betidx][idx] = temp
            self.hit_times.values[pro][betidx] = 0

        if pro <= boom_level:
            idx = self.hit_times.values[pro][betidx] // 10
            self.hit_times.values[pro][betidx] += hit_count
            score = self.pro_count.values[pro][betidx][idx] * self.betCount[betidx] * self.pro[pro]
            if score > 0:
                self.delete_fish(table_obj, fish_id, "7")
                return score
            return 0
        else:
            self.hit_times.values[pro][betidx] += hit_count
            return 0

    def get_boom_by_id(self, user_id: int, fish_id: int) -> Optional[Boom]:
        """
        This function retrieves a Boom object from a list of Boom objects based on a given user ID and fish ID, and removes it from the list.

        :param user_id: The user ID is an integer value that identifies a specific user in the system. It is used as a parameter in the `get_boom_by_id` method to search for a `Boom`
        object that matches both the user ID and the fish ID
        :type user_id: int
        :param fish_id: The `fish_id` parameter is an integer that represents the unique identifier of a fish object. It is used in the `get_boom_by_id` method to find a `Boom` object
        that has a matching `fish_id` attribute
        :type fish_id: int
        :return: The method `get_boom_by_id` returns an instance of the `Boom` class if there is a `Boom` object in the `boom_list` attribute of the class instance that has a `userId`
        attribute equal to the `user_id` argument and a `fish_id` attribute equal to the `fish_id` argument. If such a `Boom` object is found, it is
        """
        for i, boom in enumerate(self.boom_list):
            if boom.userId == user_id and boom.fish_id == fish_id:
                return self.boom_list.pop(i)
        return None

    def fishShoot(self, _pro: int, _bet: int, hit_count: int) -> None:
        """
        The function "fishShoot" takes in three parameters and does not have any implementation yet.

        :param _pro: The _pro parameter is not defined in the given function signature. It is unclear what this parameter represents without additional context or information
        :type _pro: int
        :param _bet: _bet is a parameter that represents the amount of money the player is betting on each shot in the fish shooting game
        :type _bet: int
        :param hitCount: hitCount is an integer parameter that represents the number of times the fish has been hit by the player's bullets
        :type hitCount: int
        """
        pass

    def getmoguiCount(self, userId: int) -> int:
        """
        This function returns the count of a specific user's "mogui" based on the current day.

        :param userId: an integer representing the user ID for which we want to retrieve the count of mogui (a type of virtual currency) they have
        :type userId: int
        :return: the count of mogui (a type of currency or resource) for a given user ID. If the user ID is not in the `moguiyueUserList`, it will add the user ID to the list with a
        count of 0 and the current day as the time. If the user ID is already in the list but the last time the count was updated was
        """
        nowDate = datetime.now()
        day = nowDate.day
        if userId not in self.moguiyueUserList:
            self.moguiyueUserList[userId] = {"count": 0, "time": day}
        elif self.moguiyueUserList[userId]["time"] != day:
            self.moguiyueUserList[userId]["time"] = day
            self.moguiyueUserList[userId]["count"] = 0

        return self.moguiyueUserList[userId]["count"]

    def getPool(self) -> PoolInfo:
        """
        This function returns a PoolInfo object containing information about a pool and its virtual pool.
        :return: The function `getPool` is returning an object of type `PoolInfo` which contains information about the pool and virtual pool.
        """
        return PoolInfo(pool=self.pool, virtualPool=self.virtualPool)

    def setPool(self, info: PoolInfo) -> None:
        """
        The function sets the pool and virtual pool information for an object.

        :param info: The parameter "info" is of type PoolInfo, which is likely a custom class or data structure that contains information about a pool. The method "setPool" takes this
        information and sets the "pool" and "virtualPool" attributes of the object to the corresponding values in the "info"
        :type info: PoolInfo
        """
        self.pool = info.pool
        self.virtualPool = info.virtualPool

    def costSkill(self, uid: int, info: Optional[SkillInfo]) -> int:
        """
        This function calculates the cost of a skill based on its ID and returns 0 if the skill ID is not valid.

        :param uid: an integer representing the user ID
        :type uid: int
        :param info: info is an optional parameter of type SkillInfo. It is used to provide information about a skill, including its ID (sid). If info is None or the sid is not 1 or 2,
        the function returns 0. Otherwise, it returns the cost of the skill, which is stored
        :type info: Optional[SkillInfo]
        :return: The function `costSkill` returns an integer value which is the cost of a skill. If the `info` parameter is `None` or the `sid` attribute of `info` is not 1 or 2, then
        the function returns 0. Otherwise, it returns the cost of the skill which is stored in the `skill_cost` list at the index `info.sid -
        """
        if not info or info.sid not in [1, 2]:
            return 0
        return self.skill_cost[info.sid - 1]


async def redisMessageReceived(self, message: str) -> None:
    """
    This is an asynchronous Python function that prints a message and calls two methods to get control pool and control user.

    :param message: The parameter `message` is a string that represents the message received by the server. It is passed as an argument to the `redisMessageReceived` function
    :type message: str
    """
    print("------------------------------server接收到信息了")
    print(f"message {message}")
    instance.getControlPool()
    instance.getControlUser()


def RandomNumBoth(Min: int, Max: int) -> int:
    """
    The function generates a random integer between a minimum and maximum value.

    :param Min: The minimum value of the range from which a random number will be generated
    :type Min: int
    :param Max: The maximum value that the random number can take
    :type Max: int
    :return: The function `RandomNumBoth` returns a random integer between the minimum value `Min` and the maximum value `Max`.
    """
    Range = Max - Min
    Rand = pd.core.dtypes.common.random.rand()
    return Min + round(Rand * Range)


instance = FishServer()


# Redis event listener
@sio.on('message')
async def message(ws: WebSocket, data: str) -> None:
    """
    This is an asynchronous Python function that receives a WebSocket and a string data, and then calls a method to handle the received message using Redis.

    :param ws: WebSocket - This is an object representing a WebSocket connection. It is used to send and receive messages between the client and server
    :type ws: WebSocket
    :param data: The `data` parameter is a string that represents the message received by a WebSocket connection. It is passed as an argument to the `message` function, which is an
    asynchronous function that processes the message. In this case, the `message` function calls the `redisMessageReceived` method of an
    :type data: str
    """
    await instance.redisMessageReceived(data)
