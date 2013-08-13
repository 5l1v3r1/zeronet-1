# -*- python -*-

import utility
import json
import client_json

class GameObject():
    def __init__(self):
        pass


#Player
#Stores information about a player in the game
class Player(GameObject):

    #INIT
    def __init__(self, connection, parent_game, id, name, byte_dollars, cycles, time):
        self.connection = connection
        self.parent_game = parent_game
        self.id = id
        self.name = name
        self.byte_dollars = byte_dollars
        self.cycles = cycles
        self.time = time

    #MODEL FUNCTIONS
    #talk
    #Allows a player to display a message to the screen
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

    #MODEL DATUM ACCESSORS
    #id
    #Unique Identifier
    def get_id(self):
        return id
    #name
    #Player's name
    def get_name(self):
        return name
    #byte_dollars
    #Player's points, one with more at end of game wins
    def get_byte_dollars(self):
        return byte_dollars
    #cycles
    #Player's machine cycles, used to create new Viruses
    def get_cycles(self):
        return cycles
    #time
    #The amount of time this player has before timing out
    def get_time(self):
        return time



#Mappable
#The base object for all mappable things
class Mappable(GameObject):

    #INIT
    def __init__(self, connection, parent_game, id, x, y):
        self.connection = connection
        self.parent_game = parent_game
        self.id = id
        self.x = x
        self.y = y

    #MODEL FUNCTIONS

    #MODEL DATUM ACCESSORS
    #id
    #Unique Identifier
    def get_id(self):
        return id
    #x
    #The x coordinate
    def get_x(self):
        return x
    #y
    #The y coordinate
    def get_y(self):
        return y



#Base
#The information on the base
class Base(Mappable):

    #INIT
    def __init__(self, connection, parent_game, id, x, y, owner, spawns_left):
        self.connection = connection
        self.parent_game = parent_game
        self.id = id
        self.x = x
        self.y = y
        self.owner = owner
        self.spawns_left = spawns_left

    #MODEL FUNCTIONS
    #spawn
    #Creates a Virus on the base with certain level.
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

    #MODEL DATUM ACCESSORS
    #id
    #Unique Identifier
    def get_id(self):
        return id
    #x
    #The x coordinate
    def get_x(self):
        return x
    #y
    #The y coordinate
    def get_y(self):
        return y
    #owner
    #The owner of this base
    def get_owner(self):
        return owner
    #spawns_left
    #The number of viruses this base can still spawn this turn
    def get_spawns_left(self):
        return spawns_left



#Virus
#Stores the information about a virus
class Virus(Mappable):

    #INIT
    def __init__(self, connection, parent_game, id, x, y, owner, level, moves_left, living):
        self.connection = connection
        self.parent_game = parent_game
        self.id = id
        self.x = x
        self.y = y
        self.owner = owner
        self.level = level
        self.moves_left = moves_left
        self.living = living

    #MODEL FUNCTIONS
    #move
    #
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

    #MODEL DATUM ACCESSORS
    #id
    #Unique Identifier
    def get_id(self):
        return id
    #x
    #The x coordinate
    def get_x(self):
        return x
    #y
    #The y coordinate
    def get_y(self):
        return y
    #owner
    #The owner of this Virus
    def get_owner(self):
        return owner
    #level
    #The Virus's level
    def get_level(self):
        return level
    #moves_left
    #The number of times this virus can still move this turn
    def get_moves_left(self):
        return moves_left
    #living
    #This virus is alive if the function returns a 1
    def get_living(self):
        return living



#Tile
#
class Tile(Mappable):

    #INIT
    def __init__(self, connection, parent_game, id, x, y, owner):
        self.connection = connection
        self.parent_game = parent_game
        self.id = id
        self.x = x
        self.y = y
        self.owner = owner

    #MODEL FUNCTIONS

    #MODEL DATUM ACCESSORS
    #id
    #Unique Identifier
    def get_id(self):
        return id
    #x
    #The x coordinate
    def get_x(self):
        return x
    #y
    #The y coordinate
    def get_y(self):
        return y
    #owner
    #Who owns this tile
    def get_owner(self):
        return owner


