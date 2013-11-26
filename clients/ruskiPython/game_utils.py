import time

class game_history():
    def __init__(self, ai):
        self.history = []
        self.ai = ai

    def take_snapshot(self, cache):
        snapshot = [[' ' for _ in range(self.ai.height)] for _ in range(self.ai.width)]

        for y in range(self.ai.height):
            for x in range(self.ai.width):
                if (x, y) in cache.wall_tiles.keys():
                    snapshot[x][y] = 'W'
                elif (x, y) in cache.my_viruses.keys():
                    snapshot[x][y] = 'V'
                elif (x, y) in cache.enemy_viruses.keys():
                    snapshot[x][y] = 'v'
                elif (x, y) in cache.my_bases.keys():
                    snapshot[x][y] = 'B'
                elif (x, y) in cache.enemy_bases.keys():
                    snapshot[x][y] = 'b'

        self.history.append(snapshot)
        return True

    def print_snapshot(self, snapshot):
        print('--'*self.ai.width)
        for y in range(self.ai.height):
            for x in range(self.ai.width):
                print(snapshot[x][[y]]),
            print('')
        return True

    def print_history(self):
        for snapshot in self.history:
            self.print_snapshot(snapshot)
            time.sleep(.1)
        return True

class game_cache:
    def __init__(self, ai):
        self.ai = ai

        self.my_viruses = dict()
        self.enemy_viruses = dict()

        self.my_bases = dict()
        self.enemy_bases = dict()

        self.wall_tiles = dict()
        self.my_tiles = dict()
        self.enemy_tiles = dict()

    def update(self):
        self.update_tiles()
        self.update_bases()
        self.update_viruses()
        return True

    def update_viruses(self):
        self.my_viruses = dict()
        self.enemy_viruses = dict()
        for virus in self.ai.viruses:
            if virus.owner == self.ai.my_player_id:
                self.my_viruses[(virus.x, virus.y)] = virus
            else:
                self.enemy_viruses[(virus.x, virus.y)] = virus
        return True

    def update_tiles(self):
        self.wall_tiles = dict()
        self.my_tiles = dict()
        self.enemy_tiles = dict()

        for tile in self.ai.tiles:
            if tile.owner == self.ai.my_player_id:
                self.my_tiles[(tile.x, tile.y)] = tile
            elif tile.owner == self.ai.my_player_id^1:
                self.enemy_tiles[(tile.x, tile.y)] = tile
            elif tile.owner == 3:
                self.wall_tiles[(tile.x, tile.y)] = tile

        return True

    def update_bases(self):
        self.my_bases = dict()
        self.enemy_bases = dict()

        for base in self.ai.bases:
            if base.owner == self.ai.my_player_id:
                self.my_bases[(base.x, base.y)] = base
            elif base.owner == self.ai.my_player_id^1:
                self.enemy_bases[(base.x, base.y)] = base

        return True
