#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    2016-06-18, 2016M-1.0 lzj
    Generate process report
    For bok

"""

import numpy as np
from astropy.io import fits
from common import *
from .constant import const


def report(red_path, bare_fits,
           ver_from=None, overwrite=False):
    """ Reduction result report.
    argument:
        red_path: path of output science path
        bare_fits: fits file without path and extension
        ver_from: version which data come from
        #ver_to: version which data write to
        overwrite: is set, overwrite existing output files
    returns:
        None or 0
    """
    # process global debug level
    global debug
    if "debug" not in globals():
        debug = 0
    # Version prefix
    ver_from_fix = "" if ver_from is None else "." + ver_from
    ver_to_fix = ver_from_fix


    pass
