#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    2016-06-16, 2016M-1.0 lzj
    Remove overscan
    For bok
"""

import numpy as np
import astropy.stats
from common import *
from .constant import const


def rm_os (dat, log, do_fit=False, sigma_clip=True) :
    """ Remove overscan from data, using only one side overscan
    argument:
        dat: original data from fits, data and overscan
        log: logger
        do_fit: if true, do polygon fit for overscan
        sigma_clip: use sigma-clip mean instead of median as overscan
    returns:
        data minus overscan
    """
    data = np.float64(dat[0:const.amp_ny, 0:const.amp_nx])
    osv = dat[0:const.amp_ny, const.amp_nx:const.amp_nx_os]

    if sigma_clip :
        os_mask = astropy.stats.sigma_clip(osv, axis=1, iters=3)
        os_med = np.empty(const.amp_ny, dtype=np.float64)
        for y in range(const.amp_ny) :
            os_med[y] = np.mean(osv[y, ~ os_mask[y, :]])
    else :
        os_med = np.median(osv, axis=1)

    if do_fit :
        pass

    for y in range(const.amp_ny) :
        data[y, :] -= os_med[y]

    return data

