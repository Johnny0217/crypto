from datetime import datetime
import importlib
import pandas as pd
import numpy as np
from scipy.stats import norm
import numba
import warnings
import os

warnings.filterwarnings('ignore')
from numpy.lib import stride_tricks, pad
from joblib import Parallel, delayed
from tqdm import tqdm


def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        return


def mk_data_path_from_vary_source(source):
    project_path = os.getcwd()
    save_file = 'data'
    save_path = os.path.join(project_path, save_file, source)
    check_path(save_path)
    return save_path
