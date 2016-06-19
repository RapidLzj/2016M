"""
    2016-06-18, 2016M-1.0 lzj
    Call SExrtactor to do extract source from seperated fits,
    and merge frame result
    For bok
"""


import numpy as np
from astropy.io import fits
from rm_os import rm_os
from util import *
import os, time


def photomerey(raw_path, sci_path, bare_fits, keep=False, sex_cmd="sextractor", debug=0):
    """Call SExrtactor to do extract source from seperated fits, and merge
    :param raw_path: path of raw fits file
    :param sci_path: path of output science path
    :param bare_fits: fits file without path and extention
    :param keep: keep bf corrected fits after sex, default false
    :param sex_cmd: sex command, different system may differ, default sextractor
    :param debug: debug level
    :return: n_star if OK, -1 if error
    """

    pass
