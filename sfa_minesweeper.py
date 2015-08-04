""" The Starfleet Academy mine sweeper sim expects 2 input files in the same directory as the sim.
The cuboid description file 'cuboid.in', and the move script 'moves.in'.
"""
from mine_sweeper_sim import MineSweeperSim
import argparse


parser = argparse.ArgumentParser(description='Run the mine sweeper simulator using the two files \
                                 provided on the command line.')
parser.add_argument('-f', type=str, nargs=1, help='The field file that describes \
                    the cuboid', required=True)
parser.add_argument('-s', type=str, nargs=1, help='The script of moves to \
                    perform', required=True)

args = parser.parse_args()

if __name__ == '__main__':
  cuboid_if = open(args.f[0], 'r')
  moves_if = open(args.s[0], 'r')

  sim = MineSweeperSim()
  sim.parse_cuboid(cuboid_if.readlines())
  sim.run_sim(moves_if.readlines())
