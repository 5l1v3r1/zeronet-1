import operator
import utility
import json
import client_json
import game
import game_object

## @class Player
#  @brief Stores information about a player in the game
class Player(game_object.GameObject):

    def __init__(self, connection, parent_game, byte_dollars, cycles, id, name, time):
        self._connection = connection
        self._parent_game = parent_game
        self._byte_dollars = byte_dollars
        self._cycles = cycles
        self._id = id
        self._name = name
        self._time = time

    ## @fn talk
    #  @brief Allows a player to display a message to the screen
    #  @param message The message that the player should say
    def talk(self, message):
        function_call = client_json.function_call.copy()
        function_call.update({"type": 'talk'})
        function_call.get("args").update({"actor": self.id})
        function_call.get("args").update({'message': repr(message)})

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
    def byte_dollars(self):
        return self.byte_dollars
    @property
    def cycles(self):
        return self.cycles
    @property
    def id(self):
        return self.id
    @property
    def name(self):
        return self.name
    @property
    def time(self):
        return self.time




