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


def report(sci_path, bare_fits, flags, debug=0):
    """Magnitude calibrate.
    :param sci_path: path of output science path
    :param bare_fits: fits file without path and extention
    :param flags: flag tuple of necessory steps
    :param debug: debug level
    :returns: n_mag for ok, 0 or -1 for error
    """

    pass
