# -*- python -*-
from base_ai import BaseAI
import random

## @class AI
#  @brief Class to implement competitor code

class AI(BaseAI):
    username = "Shell AI"

    ## @fn init
    #  @breif Initialization function that is ran before the game begins.
    def init(self):
        pass
    ## @fn end
    #  @breif Ending function that is ran after the game ends.
    def end(self):
        pass

    ## @fn run
    #  @breif Function is ran for each turn.
    def run(self):

        for virus in self.viruses:
            offsets = [(0,1),(0,-1),(1,0),(-1,0)]
            virus.move(random.choice(offsets))
        return True

    def __init__(self):
        BaseAI.__init__(self)
