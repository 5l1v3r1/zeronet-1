import game_objects
from .game import Game
from  util import command
from game_utils import takes, success, failure

class Mappable(Game.Object):
    _game_state_attributes = ['id', 'x', 'y']
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


class Player(Game.Object):
    _game_state_attributes = ['id', 'name', 'byte_dollars', 'cycles', 'time']
    _relations = {}
    _remotes = {}

    def __init__(self, game, **kwargs):
        print('__INIT__ PLAYER')
        Game.Object.__init__(self, game, **kwargs)
        #TODO: Fill in any work that needs to be done when an object is made
        #Common example would be setting the unit's health to maximum

        self.name = ''
        self.byte_dollars = 0
        self.cycles = self.game.config['globals']['starting_cycles']
        self.time = self.game.config['globals']['start_time']

        print('END __INIT__ PLAYER')

    def before_turn(self):
        #TODO: Fill in start of turn values
        #Common example would be giving units moves before their turn
        self.game.current_player = self
        self.cycles += self.game.get_income(self.id)
        pass

    def after_turn(self):
        #TODO: Set post-turn values
        #Common example would be zeroing unit moves after the turn
        pass

    @command
    @takes(message = unicode)
    def talk(self, message = None):
        pass


class Tile(Game.Object):
    _game_state_attributes = ['id', 'x', 'y', 'owner']
    _relations = {}
    _remotes = {}

    def __init__(self, game, x, y, owner,  **kwargs):
        Game.Object.__init__(self, game, **kwargs)
        #TODO: Fill in any work that needs to be done when an object is made
        #Common example would be setting the unit's health to maximum

        self.x = x
        self.y = y
        self.owner = owner

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

    def __init__(self, game, **kwargs):
        Game.Object.__init__(self, game, **kwargs)
        #TODO: Fill in any work that needs to be done when an object is made
        #Common example would be setting the unit's health to maximum
        self.living = 1

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

    @command
    @takes(x = int, y = int)
    def move(self, x = None, y = None):
        if self.owner != self.game.player_id:
            return 'Turn {}: You cannot control a virus that is not yours'.format(self.game.turn_number)
        elif self.moves_left <= 0:
            return 'Turn {}: Your virus {} has no moves left. ({},{}) -> ({},{})'.format(self.game.turn_number, self.id, self.x, self.y, x, y)
        elif not (0 <= x < self.game.width) or not(0 <= y < self.game.height):
            return 'Turn {}: Your virus {} cannot move off the map. ({},{}) -> ({},{})'.format(self.game.turn_number, self.id, self.x, self.y, x, y)
        elif abs(self.x - x) + abs(self.y - y) != 1:
            return 'Turn {}: Your virus {} can only move to adjacent tiles. ({},{}) -> ({},{})'.format(self.game.turn_number, self.id, self.x, self.y, x, y)
        elif self.game.grid[x][y][0].owner == 3:
            return 'Turn {}: Your virus {} cannot move onto a wall. ({},{}) -> ({},{})'.format(self.game.turn_number, self.id, self.x, self.y, x, y)

        #TODO Handle walking into bases
        for base in self.game.bases:
            pass

        #TODO Handle walking into other viruses
        for virus in self.game.viruses:
            pass

        self.game.grid[self.x][self.y].remove(self)
        self.x = x
        self.y = y
        self.moves_left -= 1
        self.game.grid[x][y].append(self)


        return True



class Base(Game.Object):
    _game_state_attributes = ['id', 'x', 'y', 'owner', 'spawns_left']
    _relations = {}
    _remotes = {}

    def __init__(self, game, x, y, owner, **kwargs):
        Game.Object.__init__(self, game, **kwargs)
        #TODO: Fill in any work that needs to be done when an object is made
        #Common example would be setting the unit's health to maximum

        self.x = x
        self.y = y
        self.owner = owner
        self.spawns_left = 0

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
    @takes(level = int)
    def spawn(self, level = None):
        player = self.game.players[self.player_id]
        cost = self.game.virus_cost(level)

        if self.owner != self.game.player_id:
            return 'Turn {}: You cannot spawn a virus on a base {} you do not own. ({},{})'.format(self.game.turn_number, self.id, self.x, self.y)
        elif level < 0:
            return 'Turn {}: You cannot spawn a virus with a level {}. ({},{})'.format(self.game.turn_number, level, self.x, self.y)
        elif player.cycles < cost:
            return 'Turn {}: You do not have enough cycles({}) to spawn this virus(level:{} cost:{}). ({},{})'.format(self.game.turn_number, player.cycles, level, cost, self.x, self.y)
        elif self.spawns_left <= 0:
            return 'Turn {}: You do not have any spawns left to spawn this virus(level:{}). ({},{}) '.format(self.game.turn_number, level, self.x, self.y)

        player.cycles -= cost
        self.spawns_left -= 1
        newVirus = self.game.add_object(Game.Object.Virus,[self.x,self.y,self.owner,level,0])

        return True






