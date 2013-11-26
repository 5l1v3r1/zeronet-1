# -*- python -*-

import operator
import utility
import json
import client_json
import game

class GameObject():
    def __init__(self):
        pass



## @class Player
#  @brief Stores information about a player in the game
class Player(GameObject):

    def __init__(self, connection, parent_game, id, name, byte_dollars, cycles, time):
        self._connection = connection
        self._parent_game = parent_game
        self._id = id
        self._name = name
        self._byte_dollars = byte_dollars
        self._cycles = cycles
        self._time = time

    ## @fn talk
    #  @brief Allows a player to display a message to the screen
    #  @param message The message that the player should say
    def talk(self, message):
        function_call = client_json.function_call.copy()
        function_call.update({"type": 'talk'})
        function_call.get("args").update({"actor": self.id})
        function_call.get("args").update({'message': repr(message)})

        utility.send_string(self.connection, json.dumps(function_call))

        received_status = False
        status = None
        while not received_status:
            message = utility.receive_string(self.connection)
            message = json.loads(message)

            if message.get("type") == "success":
                received_status = True
                status = True
            elif message.get("type") == "failure":
                received_status = True
                status = False
            if message.get("type") == "changes":
                self.parent_game.update_game(message)

        return status

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def byte_dollars(self):
        return self._byte_dollars

    @property
    def cycles(self):
        return self._cycles

    @property
    def time(self):
        return self._time




## @class Mappable
#  @brief The base object for all mappable things
class Mappable(GameObject):

    def __init__(self, connection, parent_game, id, x, y):
        self._connection = connection
        self._parent_game = parent_game
        self._id = id
        self._x = x
        self._y = y


    @property
    def id(self):
        return self._id

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y




## @class Tile
class Tile(Mappable):

    def __init__(self, connection, parent_game, id, x, y, owner):
        self._connection = connection
        self._parent_game = parent_game
        self._id = id
        self._x = x
        self._y = y
        self._owner = owner


    @property
    def id(self):
        return self._id

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def owner(self):
        return self._owner




## @class Base
#  @brief The information on the base
class Base(Mappable):

    def __init__(self, connection, parent_game, id, x, y, owner, spawns_left):
        self._connection = connection
        self._parent_game = parent_game
        self._id = id
        self._x = x
        self._y = y
        self._owner = owner
        self._spawns_left = spawns_left

    ## @fn spawn
    #  @brief Creates a Virus on the base with certain level.
    def spawn(self, level):
        function_call = client_json.function_call.copy()
        function_call.update({"type": 'spawn'})
        function_call.get("args").update({"actor": self.id})
        function_call.get("args").update({'level': repr(level)})

        utility.send_string(self.connection, json.dumps(function_call))

        received_status = False
        status = None
        while not received_status:
            message = utility.receive_string(self.connection)
            message = json.loads(message)

            if message.get("type") == "success":
                received_status = True
                status = True
            elif message.get("type") == "failure":
                received_status = True
                status = False
            if message.get("type") == "changes":
                self.parent_game.update_game(message)

        return status

    @property
    def id(self):
        return self._id

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def owner(self):
        return self._owner

    @property
    def spawns_left(self):
        return self._spawns_left




## @class Virus
#  @brief Stores the information about a virus
class Virus(Mappable):

    def __init__(self, connection, parent_game, id, x, y, owner, level, moves_left, living):
        self._connection = connection
        self._parent_game = parent_game
        self._id = id
        self._x = x
        self._y = y
        self._owner = owner
        self._level = level
        self._moves_left = moves_left
        self._living = living

    ## @fn move
    #  @param x The x coordinate to move to
    #  @param y The y coordinate to move to
    def move(self, x, y):
        function_call = client_json.function_call.copy()
        function_call.update({"type": 'move'})
        function_call.get("args").update({"actor": self.id})
        function_call.get("args").update({'x': repr(x)})
        function_call.get("args").update({'y': repr(y)})

        utility.send_string(self.connection, json.dumps(function_call))

        received_status = False
        status = None
        while not received_status:
            message = utility.receive_string(self.connection)
            message = json.loads(message)

            if message.get("type") == "success":
                received_status = True
                status = True
            elif message.get("type") == "failure":
                received_status = True
                status = False
            if message.get("type") == "changes":
                self.parent_game.update_game(message)

        return status

    @property
    def id(self):
        return self._id

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def owner(self):
        return self._owner

    @property
    def level(self):
        return self._level

    @property
    def moves_left(self):
        return self._moves_left

    @property
    def living(self):
        return self._living



