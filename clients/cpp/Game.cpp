#include "Game.h"
#include "json/json.h"
#include <iostream>
#include <fstream>
#include <sstream>

Game::Game(GameSocket& conn, std::string addr, int port, std::string name,
           int verbosity2)
{
    this->conn = conn;
    this->addr = addr;
    this->port = port;
    this->name = name;
    ai.connection = conn;
    verbosity = verbosity2;
}

bool Game::connect()
{
    return conn.open_server_connection(addr,port);
}

std::string Game::receive()
{
    std::string message = conn.rec_string();
    if(verbosity == 2)
    {
        std::cout<<"Recieved: "<<message<<std::endl;
    }
    Json::Value root;
    Json::Reader reader;
    reader.parse(message,root,false);
    if(root["type"].asString() == "changes")
    {
        update_game(message);
    }
    else if(root["type"].asString() == "player_id")
    {
        ai.my_player_id = root["args"]["id"].asInt();
    }
    else if(root["type"].asString() == "game_over")
    {
        throw GameOverException(root["args"]["winner"].asInt(),
                                root["args"]["reason"].asString());
    }
    return message;
}

std::string Game::wait_for(std::vector<std::string>& types)
{
    while(true)
    {
        std::string message = receive();
        Json::Value root;
        Json::Reader reader;
        reader.parse(message,root,false);
        for(int i = 0; i < types.size(); i++)
        {
            if(root["type"].asString() == types[i])
            {
                return message;
            }
        }
    }
}

const std::string login_string =
"{\"type\": \"login\", \"args\": {\"username\": \"\", \"connection_type\": \"botnet\"}}";

bool Game::login()
{
    Json::Value event;
    Json::Reader reader_login;
    reader_login.parse(login_string,event,false);

    event["args"]["username"] = ai.username();

    std::stringstream converter;
    std::string login_message;

    //event.asString() does not work
    converter<<event<<std::endl;
    login_message = converter.str();

    if(verbosity == 2)
    {
        std::cout<<"Sent: "<<login_message<<'\n';
    }
    conn.send_string(login_message);

    std::vector<std::string> wanted;
    wanted.push_back("success");
    wanted.push_back("failure");

    std::string message = wait_for(wanted);

    Json::Value root;
    Json::Reader reader;
    reader.parse(message,root,false);
    if(root["type"].asString() == "success")
    {
        return true;
    }
    else
    {
        return false;
    }
}

//create game constant stuff
const std::string create_game_string =
"{\"type\": \"join_game\", \"args\": {}}";

bool Game::create_game()
{
    Json::Value root;
    Json::Reader reader;
    reader.parse(create_game_string,root,false);
    root["args"]["game_name"] = name;

    std::stringstream converter;
    std::string messageSend;
    converter << root;
    messageSend = converter.str();

    if(verbosity == 2)
    {
        std::cout<<"Sent: "<<messageSend<<'\n';
    }
    conn.send_string(messageSend);

    std::vector<std::string> wanted;
    wanted.push_back("success");
    wanted.push_back("failure");

    std::string message = wait_for(wanted);

    Json::Value root2;
    Json::Reader reader2;
    reader.parse(message,root2,false);

    if(root2["type"] == "success")
    {
        name = root2["args"]["name"].asString();
        std::cout<<"Game created: "<<name<<std::endl;
        return true;
    }
    else
    {
        return false;
    }
}

bool Game::recv_player_id()
{
    std::vector<std::string> wanted;
    wanted.push_back("player_id");

    wait_for(wanted);
    return true;
}

bool Game::init_main()
{
    std::vector<std::string> wanted;
    wanted.push_back("start_game");
    wait_for(wanted);

    ai.init();
    return true;
}

bool Game::end_main()
{
    ai.end();
    return true;
}

const std::string end_turn_string =
"{\"type\": \"end_turn\", \"args\": {}}";

bool Game::main_loop()
{
    std::vector<std::string> wanted;
    wanted.push_back("start_turn");
    wanted.push_back("game_over");

    while(true)
    {
        std::string message = wait_for(wanted);
        Json::Value root;
        Json::Reader reader;
        reader.parse(message,root,false);

        if(root["type"] == "game_over")
        {
            return true;
        }

        if(ai.my_player_id == ai.player_id)
        {
            if(verbosity >= 1)
            {
                std::cout<<"Turn Number: "<<ai.turn_number<<std::endl;
            }
            ai.run();
            if(verbosity == 2)
            {
                std::cout<<"Sent: "<<end_turn_string<<'\n';
            }
            conn.send_string(end_turn_string);
        }
    }
}

const std::string get_log_string =
"{\"type\": \"get_log\", \"args\": {}}";

bool Game::get_log()
{
    if(verbosity == 2)
    {
        std::cout<<"Sent: "<<get_log_string<<'\n';
    }
    conn.send_string(get_log_string);

    std::vector<std::string> wanted;
    wanted.push_back("success");
    wanted.push_back("failure");

    std::string message = wait_for(wanted);
    Json::Value root;
    Json::Reader reader;
    reader.parse(message,root,false);

    if(root["type"] == "success")
    {
        std::string fileName = name + ".glog";
        std::ofstream fout;
        fout.open(fileName.c_str());
        fout << root["args"]["log"].asString();
        fout.close();
    }
    return true;
}

bool Game::update_game(std::string message)
{
    Json::Value root;
    Json::Reader reader;
    reader.parse(message,root,false);

    if(root["type"].asString() != "changes")
    {
        return false;
    }

    Json::Value changes = root["args"]["changes"];
    std::stringstream convert;

    for(int i = 0; i < changes.size(); i++)
    {
        convert<<changes[i];
        if(changes[i]["action"].asString() == "add")
        {
            change_add(convert.str());
        }
        else if(changes[i]["action"].asString() == "remove")
        {
            change_remove(convert.str());
        }
        else if(changes[i]["action"].asString() == "update")
        {
            change_update(convert.str());
        }
        else if(changes[i]["action"].asString() == "global_update")
        {
            change_global_update(convert.str());
        }
        convert.str(std::string());
    }

    return true;
}

bool Game::change_add(std::string change)
{
    Json::Value root;
    Json::Reader reader;
    reader.parse(change,root,false);

    Json::Value values = root["values"];
    if(false){}
    else if(root["type"].asString() == "Player")
    {
        Player temp(&conn,this, values["id"].asInt(), values["name"].asString(), values["byte_dollars"].asInt(), values["cycles"].asInt(), values["time"].asInt());
        ai.players.push_back(temp);
    }
    else if(root["type"].asString() == "Base")
    {
        Base temp(&conn,this, values["id"].asInt(), values["x"].asInt(), values["y"].asInt(), values["owner"].asInt(), values["spawns_left"].asInt());
        ai.bases.push_back(temp);
    }
    else if(root["type"].asString() == "Virus")
    {
        Virus temp(&conn,this, values["id"].asInt(), values["x"].asInt(), values["y"].asInt(), values["owner"].asInt(), values["level"].asInt(), values["moves_left"].asInt(), values["living"].asInt());
        ai.viruses.push_back(temp);
    }
    else if(root["type"].asString() == "Tile")
    {
        Tile temp(&conn,this, values["id"].asInt(), values["x"].asInt(), values["y"].asInt(), values["owner"].asInt());
        ai.tiles.push_back(temp);
    }
    else
    {
        std::cout<<"Unknown model attempted to add!!"<<std::endl;
    }
    return true;
}

bool Game::change_remove(std::string change)
{
    Json::Value root;
    Json::Reader reader;
    reader.parse(change,root,false);
    Json::Value null_value;

    int change_id = root["id"].asInt();


    for(int i = 0;i < ai.players.size();i++)
    {
        if(ai.players[i].id == change_id)
        {
            ai.players.erase(ai.players.begin()+i);
            return true;
        }
    }

    for(int i = 0;i < ai.bases.size();i++)
    {
        if(ai.bases[i].id == change_id)
        {
            ai.bases.erase(ai.bases.begin()+i);
            return true;
        }
    }

    for(int i = 0;i < ai.viruses.size();i++)
    {
        if(ai.viruses[i].id == change_id)
        {
            ai.viruses.erase(ai.viruses.begin()+i);
            return true;
        }
    }

    for(int i = 0;i < ai.tiles.size();i++)
    {
        if(ai.tiles[i].id == change_id)
        {
            ai.tiles.erase(ai.tiles.begin()+i);
            return true;
        }
    }
    return false;
}

bool Game::change_update(std::string change)
{
    Json::Value root;
    Json::Reader reader;
    reader.parse(change,root,false);
    Json::Value null_value;

    int change_id = root["id"].asInt();


    for(int i = 0;i < ai.players.size();i++)
    {
        if(ai.players[i].id == change_id)
        {
            if(root["changes"]["id"] != null_value)
            {
                ai.players[i].id = root["changes"]["id"].asInt();
            }
            if(root["changes"]["name"] != null_value)
            {
                ai.players[i].name = root["changes"]["name"].asString();
            }
            if(root["changes"]["byte_dollars"] != null_value)
            {
                ai.players[i].byte_dollars = root["changes"]["byte_dollars"].asInt();
            }
            if(root["changes"]["cycles"] != null_value)
            {
                ai.players[i].cycles = root["changes"]["cycles"].asInt();
            }
            if(root["changes"]["time"] != null_value)
            {
                ai.players[i].time = root["changes"]["time"].asInt();
            }
            return true;
        }
    }

    for(int i = 0;i < ai.bases.size();i++)
    {
        if(ai.bases[i].id == change_id)
        {
            if(root["changes"]["id"] != null_value)
            {
                ai.bases[i].id = root["changes"]["id"].asInt();
            }
            if(root["changes"]["x"] != null_value)
            {
                ai.bases[i].x = root["changes"]["x"].asInt();
            }
            if(root["changes"]["y"] != null_value)
            {
                ai.bases[i].y = root["changes"]["y"].asInt();
            }
            if(root["changes"]["owner"] != null_value)
            {
                ai.bases[i].owner = root["changes"]["owner"].asInt();
            }
            if(root["changes"]["spawns_left"] != null_value)
            {
                ai.bases[i].spawns_left = root["changes"]["spawns_left"].asInt();
            }
            return true;
        }
    }

    for(int i = 0;i < ai.viruses.size();i++)
    {
        if(ai.viruses[i].id == change_id)
        {
            if(root["changes"]["id"] != null_value)
            {
                ai.viruses[i].id = root["changes"]["id"].asInt();
            }
            if(root["changes"]["x"] != null_value)
            {
                ai.viruses[i].x = root["changes"]["x"].asInt();
            }
            if(root["changes"]["y"] != null_value)
            {
                ai.viruses[i].y = root["changes"]["y"].asInt();
            }
            if(root["changes"]["owner"] != null_value)
            {
                ai.viruses[i].owner = root["changes"]["owner"].asInt();
            }
            if(root["changes"]["level"] != null_value)
            {
                ai.viruses[i].level = root["changes"]["level"].asInt();
            }
            if(root["changes"]["moves_left"] != null_value)
            {
                ai.viruses[i].moves_left = root["changes"]["moves_left"].asInt();
            }
            if(root["changes"]["living"] != null_value)
            {
                ai.viruses[i].living = root["changes"]["living"].asInt();
            }
            return true;
        }
    }

    for(int i = 0;i < ai.tiles.size();i++)
    {
        if(ai.tiles[i].id == change_id)
        {
            if(root["changes"]["id"] != null_value)
            {
                ai.tiles[i].id = root["changes"]["id"].asInt();
            }
            if(root["changes"]["x"] != null_value)
            {
                ai.tiles[i].x = root["changes"]["x"].asInt();
            }
            if(root["changes"]["y"] != null_value)
            {
                ai.tiles[i].y = root["changes"]["y"].asInt();
            }
            if(root["changes"]["owner"] != null_value)
            {
                ai.tiles[i].owner = root["changes"]["owner"].asInt();
            }
            return true;
        }
    }
    return false;
}

bool Game::change_global_update(std::string change)
{
    Json::Value root;
    Json::Reader reader;
    reader.parse(change,root,false);
    Json::Value null_value;

    if(root["values"]["turn_number"] != null_value)
    {
        ai.turn_number = root["values"]["turn_number"].asInt();
    }
    if(root["values"]["player_id"] != null_value)
    {
        ai.player_id = root["values"]["player_id"].asInt();
    }
    if(root["values"]["game_number"] != null_value)
    {
        ai.game_number = root["values"]["game_number"].asInt();
    }
    if(root["values"]["base_cost"] != null_value)
    {
        ai.base_cost = root["values"]["base_cost"].asInt();
    }
    if(root["values"]["scale_cost"] != null_value)
    {
        ai.scale_cost = root["values"]["scale_cost"].asFloat();
    }
    if(root["values"]["width"] != null_value)
    {
        ai.width = root["values"]["width"].asInt();
    }
    if(root["values"]["height"] != null_value)
    {
        ai.height = root["values"]["height"].asInt();
    }
    return true;
}

bool Game::run()
{
    std::string game_over_message;
    if(!connect())
    {
        return false;
    }
    if(!login())
    {
        return false;
    }
    if(!create_game())
    {
        return false;
    }
    if(!recv_player_id())
    {
        return false;
    }
    if(!init_main())
    {
        return false;
    }

    try
    {
        main_loop();
    }
    catch(GameOverException e)
    {
        if(e.winner == ai.my_player_id)
        {
            game_over_message = "You Win! - " + e.reason;
        }
        else
        {
            game_over_message = "You Lose! - " + e.reason;
        }
    }
    catch(...)
    {
        game_over_message = "Game over was never reached.";
    }

    if(!end_main())
    {
        return false;
    }

    std::cout<<game_over_message<<std::endl;

    if(!get_log())
    {
        return false;
    }
    return true;
}
