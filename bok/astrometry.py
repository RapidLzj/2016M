#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    2016-06-18, 2016M-1.0 lzj
    Do astrometry, matching with UBNO-B1 catalog, and regress
    For bok
"""

import numpy as np
from astropy.io import fits
from rm_os import rm_os
from common import *
from constant import const


def astromerey(red_path, bare_fits,
               wcs_catalog=None, match_distan=0.002, recenter=False,
               ver_from=None, ver_to=None):
    """ Do astrometry, matching and regress with USNO-B1 catalog or SDSS/APASS
    argument:
        red_path: path of output science path
        bare_fits: fits file without path and extension
        wcs_catalog: reference catalog of wcs
        match_distan: distance limit for matching, default 0.002 deg, 7.2 arcsec
        recenter: use grid method to find real center, default false
    returns:
        n_wcs for stars count matched, 0 or -1 for error
    """

    # process global debug level
    global debug
    if "debug" not in globals():
        debug = 0
    # version prefix
    ver_from_fix = "" if ver_from is None else "." + ver_from
    ver_to_fix = "" if ver_to is None else "." + ver_to

pass
