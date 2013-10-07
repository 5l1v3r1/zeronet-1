import copy
import time

def get_tile(ai, x, y):
  return ai.tiles[x * ai.height + y]

class game_history:
  def __init__(self, ai, use_colors = False):
    self.use_colors = use_colors
    self.history = []
    self.ai = ai

    self.notmoving = None

    self.BLACK = 0
    self.RED = 1
    self.GREEN = 2
    self.YELLOW = 3
    self.BLUE = 4
    self.MAGENTA = 5
    self.CYAN = 6
    self.WHITE = 7

    #SET UP THE PARTS THAT ARE NOT MOVING
  def colorText(self, text, fgcolor = None, bgcolor = None):
    if self.use_colors and fgcolor and bgcolor:
      return '\x1b[3{};4{};1m'.format(fgcolor, bgcolor) + text + '\x1b[0m'
    elif self.use_colors and fgcolor:
      return '\x1b[3{};1m'.format(fgcolor) + text + '\x1b[0m'
    else:
      return text

  def set_nonmoving_elements(self):
    self.notmoving = [[[] for _ in range( self.ai.height ) ] for _ in range( self.ai.width ) ]

    for tile in self.ai.tiles:
      #Tile type 2 == nothing
      if tile.owner == 2:
        self.notmoving[tile.x][tile.y].append(' ')
      elif tile.owner == 3:
          self.notmoving[tile.x][tile.y].append(self.colorText('W', self.WHITE, self.BLUE))
      elif tile.owner == 0:
        self.notmoving[tile.x][tile.y].append(self.colorText('S', self.WHITE, self.RED))
      elif tile.owner == 1:
        self.notmoving[tile.x][tile.y].append(self.colorText('S', self.WHITE, self.BLUE))

    return

  def save_snapshot(self):
    tempGrid = copy.deepcopy(self.notmoving)

    for virus in self.ai.viruses:
      if virus.owner == 0:
          tempGrid[virus.x][virus.y].append(self.colorText('V', self.WHITE, self.MAGENTA))
      elif virus.owner == 1:
          tempGrid[virus.x][virus.y].append(self.colorText('V', self.BLACK. self.MAGENTA))

    #self.print_snapshot(tempGrid)
    self.history.append(tempGrid)
    return

  def print_snapshot(self, snapshot):
    print('--' * self.ai.width)
    for y in range(self.ai.height):
      for x in range(self.ai.width):
        if len(snapshot[x][y]) > 0:
            print(snapshot[x][y][0]),
        else:
          print(' '),
      print
    return

  def print_history(self):
    turn_number = 0
    for snapshot in self.history:
      print(turn_number/2)
      turn_number += 1
      self.print_snapshot(snapshot)
      time.sleep(.1)
