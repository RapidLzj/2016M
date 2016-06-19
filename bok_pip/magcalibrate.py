"""
    2016-06-18, 2016M-1.0 lzj
    Call SExrtactor to do extract source from seperated fits,
    and merge frame result
    For bok

"""

import math
from astropy.io import fits
import numpy as np
import time


def magcalibrate(sci_path, bare_fits, match_mode=1, mag_catalog="HM1998", match_distan=0.002, debug=0):
    """Magnitude calibrate.
    :param sci_path: path of output science path
    :param bare_fits: fits file without path and extention
    :param match_mode: mode of choose matched star, default 1 for auto, 0 for manual, 2 for all
    :param mag_catalog: use which magnitude catalog
    :param match_distan: distance limit for matching, default 0.002 deg, 7.2 arcsec
    :param debug: debug level
    :returns: n_mag for ok, 0 or -1 for error
    """

    pass