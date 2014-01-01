import game_objects
import objects
import random
import math
class Game(game_objects.Game):
    _name = 'botnet'
    _game_version = 1
    _server_version = 1
    _globals = ['base_cost', 'game_number', 'height', 'player_id', 'scale_cost', 'turn_number', 'width']
    _relations = {}
    _remotes = {}

    def __init__(self, game, **kwargs):
        game_objects.Game.__init__(self, game, **kwargs)
        self.config = self.load_config('defaults')

        #Some important stuff
        self.turn_number = -1
        self.player_id = 0
        self.game_number = -1

        #how long is this game
        self.game_length = self.config['globals']['game_length']

        #set some defaults
        self.base_cost = self.config['globals']['base_cost']
        self.scale_cost = self.config['globals']['scale_cost']
        self.width = self.config['globals']['width']
        self.height = self.config['globals']['height']

        self.max_bases = self.config['globals']['max_bases']
        self.max_walls = self.config['globals']['max_walls']

        self.grid = None

    @staticmethod
    def man_dist(x1, y1, x2, y2):
        return abs(x1-x2) + abs(y1-y2)

    def virus_cost(self, level):
        return int(self.base_cost*self.scale_cost**level)

    def before_start(self):
        #TODO: Initialize the game

        #Create any objects that should exist at the start (Tiles, for example)
        #Initialize any global values
        #At this point Player objects exist
        #(But any game-specific values will be uninitialized)

        self.grid = [[ objects.Tile(self, x=x, y=y, owner=2) for y in range(self.height)] for x in range(self.width)]

        self.create_bases()
        self.create_walls()

        pass

    def create_bases(self):
        for _ in range(self.max_bases):
            randx = random.randrange(math.floor(self.width/2))
            randy = random.randrange(self.height)
            otherx = self.width - randx - 1

            isvalid = True
            print(self.objects)
            for base in self.bases:
                if base.x == randx and base.y == randy:
                    isvalid = False

            if isvalid:
                base1 = objects.Base(self, x=randx, y=randy, owner=0, spawns_left=1)
                base2 = objects.Base(self, x=otherx, y=randy, owner=1, spawns_left=1)

        return True

    def create_walls(self):
        for _ in range(self.max_walls):
            randx = random.randrange(math.floor(self.width/2))
            randy = random.randrange(self.height)
            otherx = self.width - randx - 1

            isvalid = True
            for base in self.bases:
                if base.x == randx and base.y == randy:
                    isvalid = False

            if isvalid:
                self.grid[randx][randy].owner = 3
                self.grid[otherx][randy].owner = 3




    def before_turn(self):
        #TODO: Initialize the turn
        #turn_number and current_player will be valued for the coming turn

        #Common operations include:
        #Setting current player's units to ready to move/attack
        #Start of turn income
        #Creating units whose construction began previously
        pass

    def after_turn(self):
        #TODO: Clean up any values at the end of a turn
        #turn_number and current_player will be valued for the past turn
        #This is called before check_winner, so this is a good place for any
        #Score calculation

        #Common operations include:
        #Setting all units to no moves_left/attacks_left
        #Any end of turn costs/damage
        pass

    def check_winner(self):
        #TODO: Calculate if anyone has won and return the winner and reason
        if self.turn_number >= self.game_length:
            return self.players[0], 'won due to tie'
        else:
            return None, 'the battle continues'
