#ifndef GAME_OBJECTS_H
#define GAME_OBJECTS_H

//Forward decleration because of cyclical dependencies
class Game;

#include "network.h"
#include <string>

class GameObject
{
    public:
    GameObject(){}
};

/// @class Player
///  @brief Stores information about a player in the game
class Player : public GameObject
{
    public:
    Player(GameSocket* connection, Game* parent_game, int id, std::string name, int byte_dollars, int cycles, int time);
    Player(){}
    /// @fn talk
    ///  @brief Allows a player to display a message to the screen
    ///  @param message The message that the player should say
    bool talk(std::string message);

    int get_id();
    std::string get_name();
    int get_byte_dollars();
    int get_cycles();
    int get_time();

    //protected:
    GameSocket* connection;
    Game* parent_game;
    int id;
    std::string name;
    int byte_dollars;
    int cycles;
    int time;

};

/// @class Mappable
///  @brief The base object for all mappable things
class Mappable : public GameObject
{
    public:
    Mappable(GameSocket* connection, Game* parent_game, int id, int x, int y);
    Mappable(){}

    int get_id();
    int get_x();
    int get_y();

    //protected:
    GameSocket* connection;
    Game* parent_game;
    int id;
    int x;
    int y;

};

/// @class Base
///  @brief The information on the base
class Base : public Mappable
{
    public:
    Base(GameSocket* connection, Game* parent_game, int id, int x, int y, int owner, int spawns_left);
    Base(){}
    /// @fn spawn
    ///  @brief Creates a Virus on the base with certain level.
    bool spawn(int level);

    int get_id();
    int get_x();
    int get_y();
    int get_owner();
    int get_spawns_left();

    //protected:
    GameSocket* connection;
    Game* parent_game;
    int id;
    int x;
    int y;
    int owner;
    int spawns_left;

};

/// @class Virus
///  @brief Stores the information about a virus
class Virus : public Mappable
{
    public:
    Virus(GameSocket* connection, Game* parent_game, int id, int x, int y, int owner, int level, int moves_left, int living);
    Virus(){}
    /// @fn move
    ///  @param x The x coordinate to move to
    ///  @param y The y coordinate to move to
    bool move(int x, int y);

    int get_id();
    int get_x();
    int get_y();
    int get_owner();
    int get_level();
    int get_moves_left();
    int get_living();

    //protected:
    GameSocket* connection;
    Game* parent_game;
    int id;
    int x;
    int y;
    int owner;
    int level;
    int moves_left;
    int living;

};

/// @class Tile
class Tile : public Mappable
{
    public:
    Tile(GameSocket* connection, Game* parent_game, int id, int x, int y, int owner);
    Tile(){}

    int get_id();
    int get_x();
    int get_y();
    int get_owner();

    //protected:
    GameSocket* connection;
    Game* parent_game;
    int id;
    int x;
    int y;
    int owner;

};


#endif
