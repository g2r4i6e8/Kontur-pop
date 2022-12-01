import subprocess
import sys


def check_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except Exception as e:
        print('Error occurred while installing requirements: {}'.format(e))
        sys.exit()
