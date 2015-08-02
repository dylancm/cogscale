""" The Starfleet Academy mine sweeper sim expects 2 input files in the same directory as the sim.
The cuboid description file 'cuboid.in', and the move script 'moves.in'.
"""

mines = []
sweeper_location = []


def print_current_field():
  # for readabilities sake I'll define the following variables so that tuple indexes are more
  # easily understood
  x = 0
  y = 1
  z = 2

  # we want to find the maximum offsets in any direction of a mine from the sweeper and use those
  # values to define our x and y boundaries
  max_x_diff = 0
  max_y_diff = 0
  for mine in mines:
    x_diff = abs(sweeper_location[-1][x] - mine[x])
    max_x_diff = x_diff if x_diff > max_x_diff else max_x_diff
    y_diff = abs(sweeper_location[-1][y] - mine[y])
    max_y_diff = y_diff if y_diff > max_y_diff else max_y_diff

  # use our maxes to determin the field bounds and populate the current field
  current_field = []
  for current_y in range((max_y_diff * 2) + 1):
    current_row = []
    for current_x in range((max_x_diff * 2) + 1):
      current_row.append('.')
    current_field.append(current_row)

  # loop over our mines and insert them into the current field
  for mine in mines:
    current_field[mine[y]][mine[x]] = mine[z]

  print current_field

def parse_cuboid(rows):

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
        mines.append((col_idx, row_idx, (-1 * ord(col)) + 96))
      elif col >= 'A' and col <= 'Z':
        mines.append((col_idx, row_idx, (-1 * ord(col)) + 38))
      else:
        raise Exception('Invalid cuboid definition')

  # x and y max give us the lower right hand corner of the defined cuboid from there we can get
  # the center point as the starting location of the mine sweeper.
  sweeper_location.append((int(x_max/2), int(y_max/2), 0))
  print sweeper_location

  print_current_field()


def execute_move(move):
  print move


if __name__ == '__main__':
  cuboid_if = open('cuboid.in', 'r')
  moves_if = open('moves.in', 'r')

  parse_cuboid(cuboid_if.readlines())

  for move in moves_if.readlines():
    execute_move(move)
