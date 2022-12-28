import os
import sys

from geometry import cut_area
from tools import check_requirements, download_population, unpack_file

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Use: python population_cutter.py top left bottom right output_filename")
        print("Coordinates should be in WGS84")
        print("Output filename should have *.geojson format")
        print("Example: python population_cutter.py 45.27334396 19.79934486 45.24239696 19.85313726 NoviSad.geojson")
        # Novi Sad
        # 45.27334396 19.79934486 45.24239696 19.85313726
        sys.exit()

    # load coordinates and cast it to float
    try:
        top = float(sys.argv[1])
        left = float(sys.argv[2])
        bottom = float(sys.argv[3])
        right = float(sys.argv[4])
        output_filename = sys.argv[5]
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
    if output_filename.split('.')[-1] == 'geojson':
        output_file = os.path.join('output', output_filename)
    elif ('geojson' not in output_filename) or (output_filename.split('.')[-1] != 'geojson'):
        print("WARNING! Output filename does not belong to geojson format. Geojson extension will be added")
        output_filename = '{}.geojson'.format(output_filename)
        output_file = os.path.join('output', output_filename)
    else:
        print("FATAL ERROR! Impossible to define output filename")
        sys.exit()

    print("Output file will be stored here: {}".format(output_file))

    # define data file
    gpkg_file = os.path.join('resources', 'kontur_population.gpkg')
    if not os.path.exists(gpkg_file):
        print("WARNING! File with population is absent")
        print("It will be downloaded shortly")
        print("You will need ~9GB of memory")

        try:
            population_file = 'kontur_population_20220630.gpkg.gz'
            if not os.path.exists(os.path.join('resources', population_file)):
                os.makedirs('resources', exist_ok=True)
                print("Downloading population data... It may take some time")
                local_filename = download_population(population_file)
        except Exception as e:
            print('Error occurred while downloading population', e)
            sys.exit()

        try:
            print("Unzipping population data... It may take some time")
            if unpack_file(local_filename, gpkg_file):
                print("Population file data loaded successfully")
            else:
                raise Exception()
        except Exception as e:
            print('Error occurred while unzipping population', e)
            sys.exit()

    # cut population
    try:
        print("Cutting population inside defined area... It may take some time")
        cut_area(gpkg_file, output_file, top, left, bottom, right)
    except Exception as e:
        print('Error occurred while cutting population', e)
