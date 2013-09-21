# -*- python -*-
from base_ai import BaseAI

## @class AI
#  @brief Class to implement competitor code

class AI(BaseAI):
    username = "Shell AI"
    password = "password"

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
        for base in self.bases():
            if base.owner == self.my_player_id and base.spawnsLeft > 0:
                base.spawn(0)

        for virus in self.viruses:
            if virus.owner == self.my_player_id and virus.movesLeft > 0:
                if 2 > virus.x:
                    virus.move(virus.x +1, virus.y)
                elif 2 < virus.x:
                    virus.move(virus.x-1, virus.y)
                else:
                    if 1 > virus.y:
                        virus.move(virus.x, virus.y+1)
                    else:
                        virus.move(virus.x, virus.y-1)

        return 1

    def __init__(self):
        BaseAI.__init__(self)
