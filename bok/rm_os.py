#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    2016-06-16, 2016M-1.0 lzj
    Remove overscan
    For bok
"""

import numpy as np
from common import *
from constant import const


def rm_os (dat, log, do_fit=True) :
    """ Remove overscan from data, using only one side overscan
    argument:
        dat: original data from fits, data and overscan
        log: logger
        do_fit: if true, do polygon fit for overscan
    returns:
        data minus overscan
    """
    data = np.float32(dat[0:const.amp_ny, 0:const.amp_nx])
    os = dat[0:const.amp_ny, const.amp_nx:const.amp_nx_os]

    os_med = np.median(os, axis=1)

    if do_fit :
        pass

    for y in range(const.amp_ny) :
        data[y, :] -= os_med[y]

    return data

