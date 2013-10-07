import game_objects
import objects
import math
import time
import os

class Game(game_objects.Game):
    _name = 'botnet'
    _game_version = 1
    _server_version = 1
    _globals = ['turn_number', 'player_id', 'game_number', 'base_cost', 'scale_cost', 'width', 'height']
    _relations = {}
    _remotes = {}

    def __init__(self, game, **kwargs):
        print('__INIT__ GAME')
        game_objects.Game.__init__(self, game, **kwargs)
        #TODO: Fill in any work that needs to be done when a match is made
        #Common example would be creating the config

        self.config = self.load_config('defaults')

        self.starting_cycles = self.config['globals']['starting_cycles']
        self.cycles_per_turn = self.config['globals']['cycles_per_turn']

        self.turn_number = 0
        self.game_number = 0
        self.base_cost = self.config['globals']['base_cost']
        self.scale_cost = self.config['globals']['scale_cost']
        self.width = self.config['globals']['width']
        self.height = self.config['globals']['height']
        self.return_amount = self.config['globals']['return_amount']
        self.time_inc = self.config['globals']['time_inc']

        self.player_id = 0

        self.viruses = []

        print('END __INIT__')

    def get_tile(self, x, y):
        return self.tiles[x * self.mapHeight + y]

    def worth(self, id):
        # Calculate the worth of a player
        total = self.players[id].cycles
        for virus in self.viruses:
            if virus.owner == id:
                total += self.virus_cost(virus.level)
        return total

    def start_map (self):
        map_filenames = []
        #look through the list of map files, for every .map file, add to mapfilename list
        for filename in os.listdir("maps/"):
            if ".map" in filename:
                map_filenames.append(filename)

        #choose a random map, open it as f, then get rid of all whitespace in file, save that file as mapdata, close f
        with open(("maps/" + map_filenames[int((time.time()*1000) % len(map_filenames))]),'r') as f:
            mapdata = f.read().replace(' ','').split()
        self.width = len(mapdata[0])
        self.height = len(mapdata)
        #Need to get the attributes for the game objects before we parse the file

        #saves y data as a enumeration called row, iterates through
        #does the same for x, saved as mapSquare. mapsquare points at map[x][y]
        for y, row in enumerate(mapdata):
            for x, map_square in enumerate(row):
                #if mapSquare is an X then it is a wall, owned by 3
                if map_square == 'X':
                    #self.grid[x][y] = self.addObject(objects.Tile, [x,y,3])
                    self.grid[x][y][0].owner = 3
                #if mapSquare is a . then it is a neutral tile owned by 2
                elif map_square == '.':
                    #self.grid[x][y] = self.add_object(objects.Tile, [x,y,2])
                    self.grid[x][y][0].owner = 2
                #if mapSquare is 1, then it is a tile owned by player 1, which means
                #there's a base on top, so we add a base too
                elif map_square == '1':
                    #self.grid[x][y] = self.addObject(objects.Tile, [x,y,1])
                    self.grid[x][y][0].owner = 1
                    self.add_object(game_objects.Base(x, y, 1))
                #same as previous, only it is player 0's base/tile combo
                elif map_square =='0':
                    #self.grid[x][y] = self.add_object(objects.Tile(x, y, 0))
                    self.grid[x][y][0].owner = 0
                    self.add_object(game_objects.Base(self, x, y, 0))

    def getScore(self, id):
        path = []
        connect = {}
        closed = [[False]*self.height for _ in range(self.width)]
        offsets = [(0,1),(1,0),(0,-1),(-1,0)]
        score = 0
        for base in self.bases:
            if base.owner == id:
                score+=1
                path.append(self.grid[base.x][base.y])
                closed[base.x][base.y] = True
        while len(path)>0:
            working = path.pop()
            for offset in offsets:
                dx, dy = working.x+offset[0], working.y+offset[1]
                if 0 <= dx < self.width and 0 <= dy < self.height and not closed[dx][dy] and self.grid[dx][dy].owner == id:
                    score+=1
                    path.append(self.grid[dx][dy])
                    closed[dx][dy] = True
        return score

    def bigger_area(self):
        p1, p2 = set(), set()
        # Builds a dictionary of all controlled tiles for both players
        for tile in self.tiles:
            if tile.owner == 0:
                p1.add((tile.x, tile.y))
            elif tile.owner == 1:
                p2.add((tile.x, tile.y))
        # defines adjacency
        offsets = [(0,1), (1,0), (0,-1), (-1,0)]

        def connect(openList, available):
            # Given a list of starting points and a set of valid points, find how many are connected to the start
            size = len(openList)
            while len(openList) > 0:
                working = openList.pop()
                for offset in offsets:
                    next = working[0] + offset[0], working[1] + offset[1]
                    if next in available:
                        available.remove(next)
                        size += 1
                        openList.append(next)
            return size

        def max_area(available):
            # Given a dictionary of valid tiles
            largest = 0
            while len(available) > 0:
                next = available.pop()
                size = connect([next], available)
                if largest < size:
                    largest = size
                return largest

        p1size, p2size = max_area(p1), max_area(p2)
        if p1size > p2size:
          return 1, 0
        elif p1size < p2size:
          return 0, 1
        else:
          return 0, 0

    def virus_cost(self, level):
        return int(self.base_cost*self.scale_cost ** level)

    def get_income(self, id):
        possible = self.starting_cycles + self.turn_number / 2 * self.cycles_per_turn
        return int(math.ceil((possible - self.worth(id))*self.return_amount) + self.cycles_per_turn)

    def before_start(self):
        #TODO: Initialize the game

        #Create any objects that should exist at the start (Tiles, for example)
        #Initialize any global values
        #At this point Player objects exist
        #(But any game-specific values will be uninitialized)
        #TODO: Something is wrong here
        self.grid = [[[ self.add_object( objects.Tile(self, x, y, 2) ) ] for y in range(self.height)] for x in range(self.width)]


    def before_turn(self):
        #TODO: Initialize the turn
        #turn_number and current_player will be valued for the coming turn

        #Common operations include:
        #Setting current player's units to ready to move/attack
        #Start of turn income
        #Creating units whose construction began previously
        if self.turn_number % 2 == 0:
            score = self.bigger_area()
            self.players[0].byte_dollars += score[0]
            self.players[1].byte_dollars += score[1]

        pass

    def after_turn(self):
        #TODO: Clean up any values at the end of a turn
        #turn_number and current_player will be valued for the past turn
        #This is called before check_winner, so this is a good place for any
        #Score calculation

        #Common operations include:
        #Setting all units to no moves_left/attacks_left
        #Any end of turn costs/damage

        print('Player id: {}'.format(self.player_id))

        if self.player_id == 0:
            self.player_id = 1
        elif self.player_id == 1:
            self.player_id = 0
        else:
            print("player_id is not 0 or 1.")
        print('Player id: {}'.format(self.player_id))
        return

    def check_winner(self):
        #TODO: Calculate if anyone has won and return the winner and reason

        player1 = self.players[0]
        player2 = self.players[1]

        if self.turn_number >= self.game_length:
            if player1.byteDollars > player2.byte_dollars:
                print("0 Wins")
            elif player2.byteDollars > player1.byte_dollars:
                print("1 Wins")
            else:
                print("A Tie!")


        if self.turn_number >= self.game_length:
            return self.players[0], 'won due to tie'
        else:
            return None, 'the battle continues'
