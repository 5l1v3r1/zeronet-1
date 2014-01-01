import game_objects
from ..game import Game
from  util import command
from game_utils import takes, success, failure

from .Mappable import Mappable

class Virus(Mappable):
    _game_state_attributes = ['id', 'level', 'living', 'moves_left', 'owner', 'x', 'y']
    _relations = {}
    _remotes = {}

    def __init__(self, game, **kwargs):
        Game.Object.__init__(self, game, **kwargs)
        #TODO: Fill in any work that needs to be done when an object is made
        #Common example would be setting the unit's health to maximum

    def before_turn(self):
        #TODO: Fill in start of turn values
        #Common example would be giving units moves before their turn
        self.spawns_left = 1
        return

    def after_turn(self):
        #TODO: Set post-turn values
        #Common example would be zeroing unit moves after the turn
        self.spawns_left = 0
        return

    @command
    @takes(x = int, y = int)
    def move(self, x = None, y = None):
        if self.owner != self.game.player_id:
            return 'Turn {}: You cannot move a virus that is not yours.'.format(self.game.turn_number)
        elif self.moves_left <= 0:
            return 'Turn {}: Your virus {} has no more moves.'.format(self.game.turn_number, self.id)
        elif x == None or y == None:
            return 'Turn {}: To move your virus {}, you must supply an x and y.'.format(self.game.turn_number, self.id)
        elif not (0 <= x < self.game.width) or not (0 <= y < self.game.height):
            return 'Turn {}: You cannot move your virus {} off the map. ({},{})->({},{})'.format(self.game.turn_number, self.id, self.x, self.y, x, y)
        elif self.game.grid[x][y].owner == 3:
            return 'Turn {}: You cannot move your virus {} into a wall. ({},{})->({},{})'.format(self.game.turn_number, self.id, self.x, self.y, x, y)
        elif self.game.man_dist(self.x, self.y, x, y) != 1:
            return 'Turn {}: You can only move your virus {} to adjacent locations. ({},{})->({},{})'.format(self.game.turn_number, self.id, self.x, self.y, x, y)
        elif not self.living:
            return 'Turn {}: You cannot move a virus that is not alive'.format(self.game.turn_number)

        for base in self.game.bases:
            if base.x == x and base.y == y:
                self.remove()
                return True

        for virus in self.game.viruses:
            if virus.x == x and virus.y == y:
                if virus.owner == self.owner:
                    if virus.level != self.level:
                        return 'Turn {}: Virus {} and {} cannot combine due to different levels. {}-><-{}'.format(self.game.turn_number, self.id, virus.id, self.level, virus.level)
                    else:
                        virus.level += 1
                        virus.moves_left = 0
                        self.remove()
                        return True
                else:
                    if virus.level > self.level:
                        self.remove()
                        return True
                    elif self.level > virus.level:
                        virus.remove()
                    elif virus.level == self.level:
                        self.remove()
                        virus.remove()
                        return True

        self.x = x
        self.y = y
        self.game.grid[x][y].owner = self.owner
        self.moves_left -= 1
        return True
