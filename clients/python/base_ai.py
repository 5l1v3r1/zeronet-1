# -*- python -*-
import socket

#  @brief Class to store competitor-accessible data and functions


class BaseAI():

    def __init__(self):
        pass

    connection = None
    game_name = "botnet"

    #  @breif The player_id of the competitor.
    my_player_id = 0

    #  @brief How many turns it has been since the beginning of the game
    turn_number = None

    #  @brief Player Number; either 0 or 1 (0 is player 1 1 is player 2)
    player_id = None

    #  @brief What number game this is for the server
    game_number = None

    #  @brief BaseCost used in the virus price formula
    base_cost = None

    #  @brief Scalar used in the virus price formula
    scale_cost = None

    #  @brief The width of the map (max X value)
    width = None

    #  @brief The height of the map (max Y value)
    height = None


    #  @brief List containing all Players.
    players = []

    #  @brief List containing all Bases.
    bases = []

    #  @brief List containing all Viruses.
    viruses = []

    #  @brief List containing all Tiles.
    tiles = []


    #  @breif Accessor function for turn_number
    def get_turn_number(self):
        return self.turn_number

    #  @breif Accessor function for player_id
    def get_player_id(self):
        return self.player_id

    #  @breif Accessor function for game_number
    def get_game_number(self):
        return self.game_number

    #  @breif Accessor function for base_cost
    def get_base_cost(self):
        return self.base_cost

    #  @breif Accessor function for scale_cost
    def get_scale_cost(self):
        return self.scale_cost

    #  @breif Accessor function for width
    def get_width(self):
        return self.width

    #  @breif Accessor function for height
    def get_height(self):
        return self.height


