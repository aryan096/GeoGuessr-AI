import os
import sys
import argparse
from geoguessr_getter import GeoGetter

def main(ARGS):
    browser = ARGS.browser
    maap = ARGS.map
    gg = GeoGetter(browser, maap)

    for i in range(5):
        print("Round: ", i+1)
        t = input("Please hit enter when ready!")
        lat, lon = gg.get_coordinates()

    input("Game complete. Please hit enter to quit!")
    gg.quit()

def parse_args():
    """ Perform command-line argument parsing. """

    parser = argparse.ArgumentParser(
        description="Let's guess some locations!",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--browser',
        required=True,
        choices=['chrome', 'firefox'],
        help='''Which web browser to to used.''')
    parser.add_argument(
        '--map',
        required=True,
        choices=['europe'],
        help='''Which map to be played. (Only Europe map supported currently)''')
    parser.add_argument(
        '--visualize',
        action='store_true',
        help='''Turns on/off visual results.''')

    return parser.parse_args()


if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)