import game_objects
from ..game import Game
from  util import command
from game_utils import takes, success, failure

from .Mappable import Mappable

class Tile(Mappable):
    _game_state_attributes = ['id', 'owner', 'x', 'y']
    _relations = {}
    _remotes = {}

    def __init__(self, game, **kwargs):
        Game.Object.__init__(self, game, **kwargs)
        #TODO: Fill in any work that needs to be done when an object is made
        #Common example would be setting the unit's health to maximum

    def before_turn(self):
        #TODO: Fill in start of turn values
        #Common example would be giving units moves before their turn
        self.moves_left = 1
        return

    def after_turn(self):
        #TODO: Set post-turn values
        #Common example would be zeroing unit moves after the turn
        self.moves_left = 0

        return
