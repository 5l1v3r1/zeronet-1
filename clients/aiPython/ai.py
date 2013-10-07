# -*- python -*-
from base_ai import BaseAI
import game_utils

## @class AI
#  @brief Class to implement competitor code

class AI(BaseAI):
    username = "Shell AI"
    password = "password"

    ## @fn init
    #  @breif Initialization function that is ran before the game begins.
    def init(self):
        self.history = game_utils.game_history(ai=self, use_colors=True)
        self.history.set_nonmoving_elements()

        return
    ## @fn end
    #  @breif Ending function that is ran after the game ends.
    def end(self):
        self.history.print_history()
        pass

    ## @fn run
    #  @breif Function is ran for each turn.
    def run(self):
        print('Turn Number: {}'.format(self.turn_number))
        self.history.save_snapshot()

        for tile in self.tiles:
            if tile.owner == self.my_player_id:
                tile.spawn()

        self.history.save_snapshot()
        return

    def __init__(self):
        BaseAI.__init__(self)
