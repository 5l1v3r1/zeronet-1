# -*- python -*-
from base_ai import BaseAI
from game_utils import *
import random

## @class AI
#  @brief Class to implement competitor code

class AI(BaseAI):
    username = "Shell AI"

    ## @fn init
    #  @breif Initialization function that is ran before the game begins.
    def init(self):
        self.gc = game_cache(self)
        self.gh = game_history(self)

        pass
    ## @fn end
    #  @breif Ending function that is ran after the game ends.
    def end(self):
        self.gh.print_history()
        pass

    ## @fn run
    #  @breif Function is ran for each turn.
    def run(self):
        print('Turn {}'.format(self.turn_number))
        self.gc.update()
        self.gh.take_snapshot(self.gc)


        self.spawn_stuff()
        self.move_stuff()

        return True

    def spawn_stuff(self):
        for base in self.gc.my_bases.values():
            print('Base {}'.format(base))
            base.spawn(0)
        return True

    def move_stuff(self):
        for virus in self.gc.my_viruses.values():
            offsets = [(0,1),(0,-1),(1,0),(-1,0)]
            offset = random.choice(offsets)

            virus.move(virus.x + offset[0], virus.y + offset[1])
        return True

    def __init__(self):
        BaseAI.__init__(self)
