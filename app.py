import sys
from argparse import ArgumentParser

from service import generate_painting


def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--input', '-i', help='Path to input image file,')
    parser.add_argument('--output', '-o', help='Path for the output file.')
    parser.add_argument('--epochs', '-e', default=25, type=int, help='Number of evolution epochs.')
    parser.add_argument('--population-size', '-p', default=50, type=int, help='Population size.')
    parser.add_argument('--n-mutations', '-m', default=25, type=int, help='Number of paintings to mutate every epoch.')
    parser.add_argument('--stroke-mut-ratio', default=0.2, type=int, help='Mutation ratio for strokes.')
    parser.add_argument('--logging-every', '-l', default=1, type=int,
                        help='Number of epochs to pass for printing a log. If it is -1, do not print logs.')
    parser.add_argument('--n-strokes', '-s', default=20000, type=int, help='Number of strokes on a painting.')
    parser.add_argument('--max-age', default=10, type=int, help='Max age for staying in population.')
    parser.add_argument('--color-max-step', default=10, type=int,
                        help='Maximal step size to mutate each color element of a stroke.')
    parser.add_argument('--length-max-step', default=3, type=int,
                        help='The maximal step size to mutate a stroke length.')
    parser.add_argument('--length-min', default=3, type=int, help='The minimal length allowed.')
    parser.add_argument('--length-max', default=15, type=int, help='The maximal length allowed.')
    parser.add_argument('--width-max-step', default=3, type=int, help='The maximal step size to mutate a stroke width.')
    parser.add_argument('--width-min', default=2, type=int, help='The minimal width allowed.')
    parser.add_argument('--width-max', default=15, type=int, help='The maximal width allowed.')
    parser.add_argument('--position-max-step', default=5, type=int,
                        help='The maximal step size to mutate position coordinates of a stroke.')
    parser.add_argument('--degrees-max-step', default=10, type=int,
                        help='The maximal step size to mutate orientation degrees of a stroke.')
    parser.add_argument('--seed', default=43, type=int, help='Seed for random.')
    parser.add_argument("--show-images", action="store_true",
                        help="Whether to show images of the best image of the population every `logging-every` epochs.")
    return parser.parse_args()


if __name__ == '__main__':
    config = parse_arguments()
    sys.exit(generate_painting(config))
