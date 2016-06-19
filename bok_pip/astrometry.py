"""
    2016-06-18, 2016M-1.0 lzj
    Do astrometry, matching with UBNO-B1 catalog, and regress
    For bok
"""


import numpy as np
from astropy.io import fits
from rm_os import rm_os
from util import *
import os, time


def astromerey(sci_path, bare_fits, recenter=False, debug=0):
    """Do astrometry, matching and regress with USNO-B1 catalog
    :param sci_path: path of output science path
    :param bare_fits: fits file without path and extention
    :param recenter: use grid mathod to find real center, default false
    :param debug: debug level
    :returns: n_wcs for stars count matched, 0 or -1 for error
    """
    pass
