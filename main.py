import os
import sys

from geometry import cut_area
from tools import check_requirements

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Use: python population_cutter.py top left bottom right")
        # sample
        # 7048591.26497715 9306376.98870119 7040405.72953559 9327904.30238216
        sys.exit()

    # load coordinates and cast it to float
    try:
        top = float(sys.argv[1])
        left = float(sys.argv[2])
        bottom = float(sys.argv[3])
        right = float(sys.argv[4])
    except:
        print("FATAL ERROR! Coordinates should be float")
        sys.exit()

    # check coordinates
    if top < bottom:
        print("FATAL ERROR! Top coordinate less than bottom coordinate")
        sys.exit()
    if right < left:
        print("FATAL ERROR! Right coordinate less than left coordinate")
        sys.exit()

    # install required packages
    check_requirements()

    # create output directory
    os.makedirs('output', exist_ok=True)

    # initialize output_file
    output_file = os.path.join('output', 'population.geojson')

    # define data file)
    gpkg_file = os.path.join('resources', 'kontur_population.gpkg')
    if not os.path.exists(gpkg_file):
        print("FATAL ERROR! File with population is absent")
        sys.exit()

    # cut population
    try:
        cut_area(gpkg_file, output_file, top, left, bottom, right)
    except Exception as e:
        print('Error occurred while cutting population', e)
