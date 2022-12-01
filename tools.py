import gzip
import shutil
import subprocess
import sys
import requests
import os
import tqdm


def check_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except Exception as e:
        print('Error occurred while installing requirements: {}'.format(e))
        sys.exit()


def download_population(population_file):
    url = 'https://geodata-eu-central-1-kontur-public.s3.amazonaws.com/kontur_datasets/{}'.format(population_file)
    local_filename = os.path.join('resources', population_file)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            pbar = tqdm.tqdm(unit="MB", position=0, leave=True)
            chunk_size = 8192
            for chunk in r.iter_content(chunk_size):
                f.write(chunk)
                pbar.update(round(chunk_size/1000,))
            pbar.close()
    return local_filename


def unpack_file(input_file, gpkg_file):
    with gzip.open(input_file, 'rb') as file:
        with open(gpkg_file, 'wb') as out_file:
            shutil.copyfileobj(file, out_file)
    return os.path.exists(gpkg_file)
