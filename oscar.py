import argparse
from reader import Parser
from classes import Mineral, Vegetal, Animal
from cell import Cell
from components import Var, Sensor, Status, Field, Birth
from model import Model


def main(args):
    """main"""

    # Build model
    oscar = Model(args)

    # Get data from file
    file = open('config_files/%s.txt' % args.filename, 'r')
    parser = Parser(oscar, Var, Sensor, Status, Field, Birth, args.size)
    data = parser.read(file)

    # Give data to the model
    for name, feed in data.items(): setattr(oscar, name, feed)

    # Build world
    oscar.world = [[Cell(row, col, args.size, model=oscar)
              		for col in range(oscar.nb_col)]
             	   for row in range(oscar.nb_row)]
    oscar.can['bg'] = oscar.world_color  # GUI stuff

    # Start the loop !
    oscar.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""
            OSCAR : Outil de Simulation Comportementale par Attraction-Repulsion
            """)
    parser.add_argument('filename', type=str, default='segregation',
                        help='Name of the file you want to read')
    parser.add_argument('-v', '--tickrate', type=float, default=0.7,
                        help='Number of ms between 2 iterations (between 0 and 1)')
    parser.add_argument('-n', '--nb_tick', type=int, default=1000,
                        help='Number of iterations before the end')
    parser.add_argument('-t', '--size', type=int, default = 500,
                        help='Dimension of the screen')
    parser.add_argument('-d', '--delay', type=int, default = 8,
                        help='Number of time step to delay at the beginning')
    parser.add_argument('-sbs', '--step_by_step', action='store_true',
    					help='Let you control the simulation step-by-step (press Enter)')
    parser.add_argument('-mfr', '--max_field_range', type = int, default = 10**4,
    					help='Help for big simulation if you know that no field will have higher range')
    args = parser.parse_args()
    main(args)
