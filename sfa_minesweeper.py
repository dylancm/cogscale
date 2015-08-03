""" The Starfleet Academy mine sweeper sim expects 2 input files in the same directory as the sim.
The cuboid description file 'cuboid.in', and the move script 'moves.in'.
"""

class MineSweeperSim:

  mines_z_map = {}
  sweeper_location = []

  moves = {
    'north': (0, -1),
    'west': (-1, 0),
    'south': (0, 1),
    'east': (1, 0)
  }

  firing = {
    'alpha': [(-1, -1), (-1, 1), (1, -1), (1, 1)],
    'beta': [(-1, 0), (0, -1), (0, 1), (1, 0)],
    'gamma': [(-1, 0), (0, 0), (1, 0)],
    'delta': [(0, -1), (0, 0), (0, 1)]
  }

  move_counter = 0
  mine_passed = False
  points = 0
  shot_penalty_counter = 0
  move_penalty_counter = 0

  def print_current_field(self):
    # for readabilities sake I'll define the following variables so that tuple indexes are more
    # easily understood
    x = 0
    y = 1

    # we want to find the maximum offsets in any direction of a mine from the sweeper and use those
    # values to define our x and y boundaries. The result will be a translation on our existing
    # coordinate system with the sweeper still in the center.
    max_x_diff = 0
    max_y_diff = 0
    for mine in self.mines_z_map.keys():
      x_diff = abs(self.sweeper_location[-1][x] - mine[x])
      max_x_diff = x_diff if x_diff > max_x_diff else max_x_diff
      y_diff = abs(self.sweeper_location[-1][y] - mine[y])
      max_y_diff = y_diff if y_diff > max_y_diff else max_y_diff

    # use our maxes to determin the field bounds and populate the current field
    current_field = []
    for current_y in range((max_y_diff * 2) + 1):
      current_row = []
      for current_x in range((max_x_diff * 2) + 1):
        current_row.append('.')
      current_field.append(current_row)

    # We can use the difference between the center of our translated coordinate system and the
    # current ships location in our main coordinate system to calculate the transformation on our
    # mines.
    mine_x_offset = self.sweeper_location[-1][x] - int(((max_x_diff * 2) + 1)/2)
    mine_y_offset = self.sweeper_location[-1][y] - int(((max_y_diff * 2) + 1)/2)

    # This is ugly, but there's a corner case where the offsets can get our of range
    if mine_x_offset > max_x_diff:
      mine_x_offset *= -1
    if mine_y_offset > max_y_diff:
      mine_y_offset *= -1

    # loop over our mines and insert them into the current field
    for mine, mine_z in self.mines_z_map.items():
      current_field[mine[y] + mine_y_offset][mine[x] + mine_x_offset] = mine_z

    for row in current_field:
      print_row = []
      for col in row:
        print_row.append(str(col))
      print '\t'.join(print_row)


  def parse_cuboid(self, rows):

    # get the height of our cuboid definition
    y_max = len(rows) - 1

    # Parse the mine locations from the input
    for row_idx in range(len(rows)):
      row = rows[row_idx].strip()
      # get the width of our cuboid definition
      x_max = len(row) - 1
      for col_idx in range(len(row)):
        col = row[col_idx]
        if col == '.':
          continue
        # we can use the ascii values to determine mine 'depth'
        elif col >= 'a' and col <= 'z':
          self.mines_z_map[(col_idx, row_idx)] = (-1 * ord(col)) + 96
        elif col >= 'A' and col <= 'Z':
          self.mines_z_map[(col_idx, row_idx)] = (-1 * ord(col)) +38
        else:
          raise Exception('Invalid cuboid definition')

    # initialize our points system
    mine_count = len(self.mines_z_map.keys())
    self.points = 10 * mine_count
    self.shot_penalty_counter = 5 * mine_count
    self.move_penalty_counter = 3 * mine_count

    # x and y max give us the lower right hand corner of the defined cuboid from there we can get
    # the center point as the starting location of the mine sweeper.
    self.sweeper_location.append((int(x_max/2), int(y_max/2), 0))

  def execute_move(self, move):
    # for readabilities sake I'll define the following variables so that tuple indexes are more
    # easily understood
    x = 0
    y = 1
    z = 2

    # parse the step and see if it is a valid movement for firing pattern
    steps = move.strip().split(' ')
    for step in steps:
      if step in self.moves.keys():
        # update the sweeper's location for the given movement
        cur_loc = self.sweeper_location[-1]
        move = self.moves[step]
        self.sweeper_location.append((cur_loc[x] + move[x], cur_loc[y] + move[y], cur_loc[z]))

        # points accounting
        if self.move_penalty_counter:
          self.points -= 2
          self.move_penalty_counter -= 1
      elif step in self.firing.keys():
        pattern = self.firing[step]
        cur_loc = self.sweeper_location[-1]
        for off_set in pattern:
          torp_loc = (cur_loc[x] + off_set[x], cur_loc[y] + off_set[y])
          if torp_loc in self.mines_z_map.keys():
            del self.mines_z_map[torp_loc]

        # points accounting
        if self.shot_penalty_counter:
          self.points -= 5
          self.shot_penalty_counter -= 1

  def increment_move(self):
    self.move_counter += 1
    for mine, z in self.mines_z_map.items():
      if z + 1 >= 0:
        self.mine_passed = True
      self.mines_z_map[mine] = z + 1

  def run_sim(self, moves):
    """ Handles running the sim from the input and providing output
    """

    for move in moves:
      # check if we've all mines are gone
      if len(self.mines_z_map.keys()) == 0:
        self.points = 1

      print 'Step {0}'.format(self.move_counter + 1)
      print
      self.print_current_field()
      print
      print move.strip()
      print
      self.execute_move(move)
      self.increment_move()
      self.print_current_field()
      print
      if self.mine_passed:
        # if we pass a mine we fail with 0 points
        print 'fail (0)'
        break

    # if we've done all the moves form the script and there are still mines we fail with - points
    if len(self.mines_z_map.keys()) != 0:
      print 'fail (0)'

    print 'pass ({0})'.format(self.points)


if __name__ == '__main__':
  cuboid_if = open('cuboid.in', 'r')
  moves_if = open('moves.in', 'r')

  sim = MineSweeperSim()
  sim.parse_cuboid(cuboid_if.readlines())
  sim.run_sim(moves_if.readlines())
