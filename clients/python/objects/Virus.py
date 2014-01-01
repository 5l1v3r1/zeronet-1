import operator
import utility
import json
import client_json
import json
import game
from game_object import GameObject
from .Mappable import Mappable

## @class Virus
#  @brief Stores the information about a virus
class Virus(Mappable):

    def __init__(self, connection, parent_game, id, level, living, moves_left, owner, x, y):
        self._connection = connection
        self._parent_game = parent_game
        self._id = id
        self._level = level
        self._living = living
        self._moves_left = moves_left
        self._owner = owner
        self._x = x
        self._y = y

    ## @fn move
    #  @param x The x coordinate to move to
    #  @param y The y coordinate to move to
    def move(self, x, y):
        function_call = client_json.function_call.copy()
        function_call.update({"type": 'move'})
        function_call.get("args").update({"actor": self.id})
        function_call.get("args").update({'x': repr(x)})
        function_call.get("args").update({'y': repr(y)})

        utility.send_string(self._connection, json.dumps(function_call))

        received_status = False
        status = None
        while not received_status:
            message = utility.receive_string(self._connection)
            message = json.loads(message)

            if message.get("type") == "success":
                received_status = True
                status = True
            elif message.get("type") == "failure":
                received_status = True
                status = False
            if message.get("type") == "changes":
                self._parent_game.update_game(message)

        return status

    @property
    def id(self):
        return self.id
    @property
    def level(self):
        return self.level
    @property
    def living(self):
        return self.living
    @property
    def moves_left(self):
        return self.moves_left
    @property
    def owner(self):
        return self.owner
    @property
    def x(self):
        return self.x
    @property
    def y(self):
        return self.y




