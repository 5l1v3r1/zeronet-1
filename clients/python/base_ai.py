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

    #  @brief The name of this match on the server
    game_name = None

    #  @brief Player Number; either 0 or 1 (0 is player 1 1 is player 2)
    player_id = None

    #  @brief The time a player has when the game begins in seconds
    start_time = None

    #  @brief How much extra time a player gets when their turn begins
    time_increment = None


    #  @brief List containing all Players.
    players = []

    #  @brief List containing all Tiles.
    tiles = []


    #  @breif Accessor function for turn_number
    def get_turn_number(self):
        return self.turn_number

    #  @breif Accessor function for game_name
    def get_game_name(self):
        return self.game_name

    #  @breif Accessor function for player_id
    def get_player_id(self):
        return self.player_id

    #  @breif Accessor function for start_time
    def get_start_time(self):
        return self.start_time

    #  @breif Accessor function for time_increment
    def get_time_increment(self):
        return self.time_increment


