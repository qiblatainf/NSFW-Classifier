
# Impprting Libraries & Packages
import datetime
import time
import cv2
from keras.models import load_model
import numpy as np
from collections import deque
import warnings
import sys
import config
import argparse

warnings.filterwarnings("ignore")





if __name__ == "__main__":
    # initialize ArgumentParser class of argparse
    parser = argparse.ArgumentParser()

    # currently, we only need filepath to the image
    parser.add_argument("--file_path", type=str)

    # read the arguments from the command line
    args = parser.parse_args()


    # run the predict specified by command line arguments
    startTime = time.time()
    predict(file_path=args.file_path)
