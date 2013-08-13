# -*- python -*-

import utility
import json
import client_json

class GameObject():
    def __init__(self):
        pass


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



#Player
#Stores information about a player in the game
class Player(GameObject):

    #INIT
    def __init__(self, connection, parent_game, id, name, time):
        self.connection = connection
        self.parent_game = parent_game
        self.id = id
        self.name = name
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
    #time
    #The amount of time this player has before timing out
    def get_time(self):
        return time



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


