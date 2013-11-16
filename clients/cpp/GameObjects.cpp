#include "GameObjects.h"
#include "json/json.h"
#include "Game.h"
#include <sstream>
#include <iostream>
#include <string>

const std::string function_call =
"{\"type\": \"command_name\", \"args\": {\"actor\": 0}}";

Player::Player(GameSocket* connection, Game* parent_game, int id, std::string name, int byte_dollars, int cycles, int time)
{
    this->connection = connection;
    this->parent_game = parent_game;
    this->id = id;
    this->name = name;
    this->byte_dollars = byte_dollars;
    this->cycles = cycles;
    this->time = time;
}

bool Player::talk(std::string message)
{
    std::stringstream convert;
    Json::Value root;
    Json::Reader reader_login;
    reader_login.parse(function_call,root,false);
    root["type"] = "talk";
    root["args"]["actor"] = id;
    convert << message;
    root["args"]["message"] = convert.str();
    convert.str(std::string());

    convert << root;
    //std::cout << root << std::endl;

    if(verbosity == 2)
    {
        std::cout<<"Sent: "<<convert.str()<<'\n';
    }
    connection->send_string(convert.str());
    bool recievedStatus = false;
    bool status;

    while(!recievedStatus)
    {
        std::string message = connection->rec_string();
        Json::Value root2;
        Json::Reader reader_login2;
        reader_login2.parse(function_call,root2,false);
        if(root2["type"] == "success")
        {
            recievedStatus = true;
            status = true;
        }
        else if(root2["type"] == "failure")
        {
            recievedStatus = true;
            status = false;
        }
        else if(root2["type"] == "changes")
        {
            parent_game->update_game(message);
        }
    }
    return status;
}

int Player::get_id()
{
    return id;
}

std::string Player::get_name()
{
    return name;
}

int Player::get_byte_dollars()
{
    return byte_dollars;
}

int Player::get_cycles()
{
    return cycles;
}

int Player::get_time()
{
    return time;
}


Mappable::Mappable(GameSocket* connection, Game* parent_game, int id, int x, int y)
{
    this->connection = connection;
    this->parent_game = parent_game;
    this->id = id;
    this->x = x;
    this->y = y;
}


int Mappable::get_id()
{
    return id;
}

int Mappable::get_x()
{
    return x;
}

int Mappable::get_y()
{
    return y;
}


Tile::Tile(GameSocket* connection, Game* parent_game, int id, int x, int y, int owner)
{
    this->connection = connection;
    this->parent_game = parent_game;
    this->id = id;
    this->x = x;
    this->y = y;
    this->owner = owner;
}


int Tile::get_id()
{
    return id;
}

int Tile::get_x()
{
    return x;
}

int Tile::get_y()
{
    return y;
}

int Tile::get_owner()
{
    return owner;
}


Base::Base(GameSocket* connection, Game* parent_game, int id, int x, int y, int owner, int spawns_left)
{
    this->connection = connection;
    this->parent_game = parent_game;
    this->id = id;
    this->x = x;
    this->y = y;
    this->owner = owner;
    this->spawns_left = spawns_left;
}

bool Base::spawn(int level)
{
    std::stringstream convert;
    Json::Value root;
    Json::Reader reader_login;
    reader_login.parse(function_call,root,false);
    root["type"] = "spawn";
    root["args"]["actor"] = id;
    convert << level;
    root["args"]["level"] = convert.str();
    convert.str(std::string());

    convert << root;
    //std::cout << root << std::endl;

    if(verbosity == 2)
    {
        std::cout<<"Sent: "<<convert.str()<<'\n';
    }
    connection->send_string(convert.str());
    bool recievedStatus = false;
    bool status;

    while(!recievedStatus)
    {
        std::string message = connection->rec_string();
        Json::Value root2;
        Json::Reader reader_login2;
        reader_login2.parse(function_call,root2,false);
        if(root2["type"] == "success")
        {
            recievedStatus = true;
            status = true;
        }
        else if(root2["type"] == "failure")
        {
            recievedStatus = true;
            status = false;
        }
        else if(root2["type"] == "changes")
        {
            parent_game->update_game(message);
        }
    }
    return status;
}

int Base::get_id()
{
    return id;
}

int Base::get_x()
{
    return x;
}

int Base::get_y()
{
    return y;
}

int Base::get_owner()
{
    return owner;
}

int Base::get_spawns_left()
{
    return spawns_left;
}


Virus::Virus(GameSocket* connection, Game* parent_game, int id, int x, int y, int owner, int level, int moves_left, int living)
{
    this->connection = connection;
    this->parent_game = parent_game;
    this->id = id;
    this->x = x;
    this->y = y;
    this->owner = owner;
    this->level = level;
    this->moves_left = moves_left;
    this->living = living;
}

bool Virus::move(int x, int y)
{
    std::stringstream convert;
    Json::Value root;
    Json::Reader reader_login;
    reader_login.parse(function_call,root,false);
    root["type"] = "move";
    root["args"]["actor"] = id;
    convert << x;
    root["args"]["x"] = convert.str();
    convert.str(std::string());
    convert << y;
    root["args"]["y"] = convert.str();
    convert.str(std::string());

    convert << root;
    //std::cout << root << std::endl;

    if(verbosity == 2)
    {
        std::cout<<"Sent: "<<convert.str()<<'\n';
    }
    connection->send_string(convert.str());
    bool recievedStatus = false;
    bool status;

    while(!recievedStatus)
    {
        std::string message = connection->rec_string();
        Json::Value root2;
        Json::Reader reader_login2;
        reader_login2.parse(function_call,root2,false);
        if(root2["type"] == "success")
        {
            recievedStatus = true;
            status = true;
        }
        else if(root2["type"] == "failure")
        {
            recievedStatus = true;
            status = false;
        }
        else if(root2["type"] == "changes")
        {
            parent_game->update_game(message);
        }
    }
    return status;
}

int Virus::get_id()
{
    return id;
}

int Virus::get_x()
{
    return x;
}

int Virus::get_y()
{
    return y;
}

int Virus::get_owner()
{
    return owner;
}

int Virus::get_level()
{
    return level;
}

int Virus::get_moves_left()
{
    return moves_left;
}

int Virus::get_living()
{
    return living;
}



