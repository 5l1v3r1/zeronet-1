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
        if self.id == self.game.playerID:
            if self.game.turnNumber < self.game.turnLimit:
                self.cycles += self.game.getIncome(self.id)
        pass

    def after_turn(self):
        #TODO: Set post-turn values
        #Common example would be zeroing unit moves after the turn
        pass

    @command
    @takes(message = unicode)
    def talk(self, message = None):
        if message:
            print(message)
        return


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


class Base(Game.Object):
    _game_state_attributes = ['id', 'x', 'y', 'owner', 'spawns_left']
    _relations = {}
    _remotes = {}

    def before_turn(self):
        #TODO: Fill in start of turn values
        #Common example would be giving units moves before their turn
        if self.owner == self.game.player_id:
            self.spawnsLeft = 1
        else:
            self.spawnsLeft = 0
        pass

    def after_turn(self):
        #TODO: Set post-turn values
        #Common example would be zeroing unit moves after the turn

        return

    @command
    @takes(level = int)
    def spawn(self, level = None):
        player = self.game.player[self.owner]
        cost = self.game.virusCost(level)

        if self.owner != self.game.playerID:
            return "You cannot spawn a virus at the opponents base."
        elif level < 0:
            return "A virus must have a level greater than zero."
        elif player.cycles < cost:
            return "You do not have enough cycles to create this virus."
        elif self.spawns_left < 1:
            return "A base can only spawn one virus per turn."
        else:
            for virus in self.game.objects.viruses:
                if virus.x == self.x and virus.y == self.y:
                    return "You cannot spawn a virus on an occupied base."

        player.cycles -= cost
        self.spawnsLeft -= 1
        newVirus = self.game.add_object(Virus, [self.x, self.y, self.owner. level, 0])
        return True;


class Virus(Game.Object):
    _game_state_attributes = ['id', 'x', 'y', 'owner', 'level', 'moves_left', 'living']
    _relations = {}
    _remotes = {}

    def before_turn(self):
        #TODO: Fill in start of turn values
        #Common example would be giving units moves before their turn

        if self.owner == self.game.player_id:
            self.movesLeft = 1
        else:
            self.movesLeft = 0
        return

    def after_turn(self):
        #TODO: Set post-turn values
        #Common example would be zeroing unit moves after the turn
        pass

    @command
    @takes(x = int, y = int)
    def move(self, x = None, y = None):
        if self.owner != self.game.player_id:
            return "You cannot move a virus that is not yours."
        elif x == None or y == None:
            return "You must specify where you want to move the virus"
        elif self.movesLeft <= 0:
            return "The virus you are attempting to move has no turns left."
        elif not (0 <= x < self.game.width) or not (0 <= y < self.game.height):
            return "You are attempting to move the virus off the map."
        elif self.game.grid[x][y].owner ==  3:
            return "You are attempting to move the virus into a wall."
        elif abs(self.x-x) + abs(self.y-y) != 1:
            return "You can only move a virus one space away."

        for base in self.game.bases:
            if base.x == x and base.y == y:
                self.game.remove_object(self)
                return True

        for virus in self.game.viruses:
            if virus.x == x and virus.y == y:
                if virus.owner == self.owner:
                    #Movement into friendly virus
                    if virus.level != self.level:
                        return "You cannot combine units of different levels."
                    else:
                        virus.level += 1
                        virus.movesLeft = 0
                        self.game.remove_object(self)
                        return True
                else:
                    #Attacking an enemy virus
                    if virus.level > self.level:
                        self.game.remove_object(self)
                        return True
                    elif self.level > virus.level:
                        self.game.remove_object(self)
                    elif virus.level == self.level:
                        self.game.remove_object(virus)
                        self.game.remove_object(self)
                        return True

        self.x, self.y = x, y
        self.game.grid[x][y].owner = self.owner
        self.movesLeft -= 1
        return True


