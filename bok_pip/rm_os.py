"""
    2016-06-16, 2016M-1.0 lzj
    Remove overscan
    For bok
"""

import numpy as np


def rm_os ( dat, no_fit = True, debug=0 ) :
    'Remove overscan from data, using only one side overscan'

    nx, ny, nyo = 2048, 2016, 2036

    data = np.float32(dat[0:nx, 0:ny])
    os = dat[0:nx, ny:nyo]

    os_med = np.median(os, axis=1)

    if not no_fit :
        pass

    for l in range(nx) :
        data[l, :] -= os_med[l]

    return data

