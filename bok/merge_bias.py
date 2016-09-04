#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    2016-06-16, 2016M-1.0 lzj
    Bias and flat merge
    For bok
"""


import numpy as np
from astropy.io import fits
from common import *
from .rm_os import rm_os
from .constant import const


def merge_bias(bias_list, out_bias_file, basedir="", overwrite=False):
    """ Merge bias with median values
    args:
        bias_list: bias file list or list file
        out_bias_file: output filename
        basedir: path added to files in list
        debug: debug level
        overwrite: if target exists, overwrite or not
    returns:
        1 if ok, 0 or -1 for error
    """
    # process global debug level
    global debug
    if "debug" not in globals():
        debug = 0
    log = logger(out_bias_file[0:-4]+'log', "MergeBias", debug)

    (files, n_file) = list_expand(bias_list, basedir=basedir, log=log)
    if not is_list_exists(files, log=log) :
        log.write("NOT all files in list exist. Abort!", -1)
        return -1

    if not overwrite_check(overwrite, [out_bias_file], log=log) :
        log.write("Abort!", -1)
        return -1

    data_cube = np.empty([n_file, const.n_amp, const.amp_ny, const.amp_nx], dtype=np.float64)

    # load data into cube, overscan removed
    for f in range(n_file) :
        log.write("#{:>3d}/{:<3d} Loading: {:s}".format(f + 1, n_file, files[f]))
        hdulist = fits.open(files[f])
        for a in range(const.n_amp) :
            data_cube[f, a] = rm_os(hdulist[a + 1].data, log)
        hdulist.close()

    # get median
    log.write("Merging....")
    bias_data = np.float32(np.median(data_cube, axis=0))

    # generate fits structure and save to new file
    new_hdulist = fits.HDUList()
    pri_hdu = fits.PrimaryHDU(header=hdulist[0].header)
    #pri_hdu.header.append(("BIASCNT", n_file, "Bias files count used in this merge"))
    #pri_hdu.header.append(("BIASDATE", now_str(), "Bias process time"))
    pri_hdu.header.update(BIASCNT=(n_file, "Bias files count used in this merge"),
                          BIASDATE=(now_str(), "Bias process time"))
    new_hdulist.append( pri_hdu )
    for a in range(const.n_amp) :
        img_hdu = fits.ImageHDU(data=bias_data[a], header=hdulist[a + 1].header)
        new_hdulist.append(img_hdu)

    log.write('Save bias to `{}`'.format(out_bias_file))
    new_hdulist.writeto(out_bias_file, clobber=overwrite)

    log.close()
