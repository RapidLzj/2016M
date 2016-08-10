#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    2016-06-18, 2016M-1.0 lzj
    Magnitude calibration according to catalog
    For bok

"""

import numpy as np
from astropy.io import fits
from rm_os import rm_os
from common import *
from constant import const


def magcalibrate(red_path, bare_fits,
                 mag_catalog="catalog/HM1998", match_mode=1, match_distan=0.002,
                 ver_from=None, ver_to=None):
    """ Magnitude calibrate.
    argument:
        red_path: path of output science path
        bare_fits: fits file without path and extension
        mag_catalog: use which magnitude catalog
        match_mode: mode of choose matched star, default 1 for auto, 0 for manual, 2 for all
        match_distan: distance limit for matching, default 0.002 deg, 7.2 arcsec
    returns:
    n_mag for ok, 0 or -1 for error
    """
    # process global debug level
    global debug
    if "debug" not in globals():
        debug = 0
    # version prefix
    ver_from_fix = "" if ver_from is None else "." + ver_from
    ver_to_fix = "" if ver_to is None else "." + ver_to

pass