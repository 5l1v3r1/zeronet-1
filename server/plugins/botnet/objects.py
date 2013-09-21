import game_objects
from .game import Game
from  util import command
from game_utils import takes, success, failure

class Player(Game.Object):
    _game_state_attributes = ['id', 'name', 'byte_dollars', 'cycles', 'time']
    _relations = {}
    _remotes = {}

    def before_turn(self):
        #TODO: Fill in start of turn values
        #Common example would be giving units moves before their turn
        pass

    def after_turn(self):
        #TODO: Set post-turn values
        #Common example would be zeroing unit moves after the turn
        pass

    @command
    @takes(message = unicode)
    def talk(self, message = None):
        pass


class Mappable(Game.Object):
    _game_state_attributes = ['id', 'x', 'y']
    _relations = {}
    _remotes = {}

    def before_turn(self):
        #TODO: Fill in start of turn values
        #Common example would be giving units moves before their turn
        pass

    def after_turn(self):
        #TODO: Set post-turn values
        #Common example would be zeroing unit moves after the turn
        pass


class Tile(Game.Object):
    _game_state_attributes = ['id', 'x', 'y', 'owner']
    _relations = {}
    _remotes = {}

    def before_turn(self):
        #TODO: Fill in start of turn values
        #Common example would be giving units moves before their turn
        pass

    def after_turn(self):
        #TODO: Set post-turn values
        #Common example would be zeroing unit moves after the turn
        pass


class Virus(Game.Object):
    _game_state_attributes = ['id', 'x', 'y', 'owner', 'level', 'moves_left', 'living']
    _relations = {}
    _remotes = {}

    def before_turn(self):
        #TODO: Fill in start of turn values
        #Common example would be giving units moves before their turn
        pass

    def after_turn(self):
        #TODO: Set post-turn values
        #Common example would be zeroing unit moves after the turn
        pass

    @command
    @takes(x = int, y = int)
    def move(self, x = None, y = None):
        pass


class Base(Game.Object):
    _game_state_attributes = ['id', 'x', 'y', 'owner', 'spawns_left']
    _relations = {}
    _remotes = {}

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
        pass


