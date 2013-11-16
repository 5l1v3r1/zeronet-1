#ifndef BASEAI_H
#define BASEAI_H

#include <vector>
#include <string>
#include "network.h"
#include "GameObjects.h"

/// @class BaseAI
///  @brief Class to store competitor-accessible data and functions

class BaseAI
{
    public:
    GameSocket connection;
    std::string game_name;

    /// @var my_player_id
    ///  @breif The player_id of the competitor.
    int my_player_id;

    /// @var turn_number
    ///  @brief How many turns it has been since the beginning of the game
    int turn_number;
    /// @var player_id
    ///  @brief Player Number; either 0 or 1 (0 is player 1 1 is player 2)
    int player_id;
    /// @var game_number
    ///  @brief What number game this is for the server
    int game_number;
    /// @var base_cost
    ///  @brief BaseCost used in the virus price formula
    int base_cost;
    /// @var scale_cost
    ///  @brief Scalar used in the virus price formula
    float scale_cost;
    /// @var width
    ///  @brief The width of the map (max X value)
    int width;
    /// @var height
    ///  @brief The height of the map (max Y value)
    int height;

    /// @var players
    ///  @brief List containing all Players.
    std::vector<Player> players;
    /// @var tiles
    ///  @brief List containing all Tiles.
    std::vector<Tile> tiles;
    /// @var bases
    ///  @brief List containing all Bases.
    std::vector<Base> bases;
    /// @var viruses
    ///  @brief List containing all Viruses.
    std::vector<Virus> viruses;

    int get_turn_number(){return turn_number;}
    int get_player_id(){return player_id;}
    int get_game_number(){return game_number;}
    int get_base_cost(){return base_cost;}
    float get_scale_cost(){return scale_cost;}
    int get_width(){return width;}
    int get_height(){return height;}

    BaseAI();
};

#endif
