import game_objects
from ..game import Game
from  util import command
from game_utils import takes, success, failure

from .Mappable import Mappable

class Base(Mappable):
    _game_state_attributes = ['id', 'owner', 'spawns_left', 'x', 'y']
    _relations = {}
    _remotes = {}

    def __init__(self, game, **kwargs):
        Game.Object.__init__(self, game, **kwargs)
        #TODO: Fill in any work that needs to be done when an object is made
        #Common example would be setting the unit's health to maximum

    def before_turn(self):
        #TODO: Fill in start of turn values
        #Common example would be giving units moves before their turn
        pass

    def after_turn(self):
        #TODO: Set post-turn values
        #Common example would be zeroing unit moves after the turn
        pass

    @command
    @takes(level = int)
    def spawn(self, level = None):
        player = self.game.players[self.owner]
        cost = self.game.virus_cost(level)


        if self.owner != self.game.player_id:
            return 'Turn {}: You cannot spawn a virus on an opponent\'s base.'.format(self.game.turn_number)
        elif level == None:
            return 'Turn {}: You cannot spawn a virus with a level of None.'.format(self.game.turn_number)
        elif level < 0:
            return 'Turn {}: You cannot spawn a virus with a level less than zero {}.'.format(self.game.turn_number, level)
        elif player.cycles < cost:
            return 'Turn {}: You do not have enough cycles({}) to spawn this virus with cost {}.'.format(self.game.turn_number, player.cycles, cost)
        elif self.spawns_left <= 0:
            return 'Turn {}: You can only spawn one virus per turn per base.'.format(self.game.turn_number)

        for virus in self.game.viruses:
            if virus.x == self.x and virus.y == self.y:
                return 'Turn {}: You cannot spawn a virus on an occupied base.'.format(self.game.turn_number)

        player.cycles -= cost
        self.spawns_left -= 1

        new_virus = game_objects.Virus(self, x=x, y=y, level=level, moves_left=0, living=True)

        return True


