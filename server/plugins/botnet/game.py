import game_objects
import objects

class Game(game_objects.Game):
    _name = 'botnet'
    _game_version = 1
    _server_version = 1
    _globals = ['turn_number', 'player_id', 'game_number', 'base_cost', 'scale_cost', 'width', 'height']
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

        self.grid = None



    def before_start(self):
        #TODO: Initialize the game

        #Create any objects that should exist at the start (Tiles, for example)
        #Initialize any global values
        #At this point Player objects exist
        #(But any game-specific values will be uninitialized)

        self.grid = [[[ self.add_object( objects.Tile(self, x, y, 2) ) ] for y in range(self.height)] for x in range(self.width)]

        pass

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
