import game_objects
import objects

class Game(game_objects.Game):
    _name = 'botnet'
    _game_version = 1
    _server_version = 1
    _globals = ['turn_number', 'player_id', 'game_number', 'base_cost', 'scale_cost', 'width', 'height']
    _relations = {}
    _remotes = {}

    def before_start(self):
        #TODO: Initialize the game

        #Create any objects that should exist at the start (Tiles, for example)
        #Initialize any global values
        #At this point Player objects exist
        #(But any game-specific values will be uninitialized)
        config = self.load_config('defaults')
        self.game_length = config['globals']['game_length']

        self.turn_number = 0
        self.player_id = 0
        self.width = config['globals']['width']
        self.height = config['globals']['height']


    def before_turn(self):
        #TODO: Initialize the turn
        #turn_number and current_player will be valued for the coming turn

        #Common operations include:
        #Setting current player's units to ready to move/attack
        #Start of turn income
        #Creating units whose construction began previously

        #self.turn_number += 1

        if self.turn_number % 2 == 0:
            score = [10, 10]
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

        if self.player_id == 0:
            self.player_id = 1
        elif self.player_id == 1:
            self.player_id = 0
        else:
            print("player_id is not 0 or 1.")

        pass

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
