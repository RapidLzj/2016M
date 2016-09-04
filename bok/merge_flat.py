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


def merge_flat ( flat_list, bias_file, out_flat_file, basedir="", overwrite=False) :
    """ Merge flat with normalized median values
    argument:
        flat_list: flat file list or list file
        bias_file: bias fits file
        out_flat_file: output filename
        basedir: path added to files in list
        overwrite: overwrite if exists
    returns:
        1 if ok, 0 or -1 for error
    """
    # process global debug level
    global debug
    if "debug" not in globals():
        debug = 0
    log = logger(out_flat_file[0 :-4] + 'log', "MergeFlat", debug)

    (files, n_file) = list_expand(flat_list, basedir=basedir, log=log)
    if not is_list_exists(files, log=log):
        log.write("NOT all files in list exist", -1)
        return -1
    if not os.path.isfile(bias_file) :
        log.write("bias file NOT EXIST", -1)
        return -1

    if not overwrite_check(overwrite, [out_flat_file], log=log) :
        log.write("Abort!", -1)
        return -1

    data_cube = np.empty([n_file, const.n_amp, const.amp_ny, const.amp_nx], dtype=np.float64)

    biashdu = fits.open(bias_file)

    # load data into cube, overscan removed
    for f in range(n_file) :
        log.write("#{:>3d}/{:<3d} Loading: {:s}".format(f+1, n_file, files[f]))
        hdulist = fits.open(files[f])
        for a in range(const.n_amp) :
            # remove overscan and bias
            data_one = rm_os(hdulist[a + 1].data, log) - biashdu[a + 1].data
            # normalize
            #data_med = np.median(data_one)
            data_cube[f, a] = data_one# / data_med
        data_med = np.median(data_cube[f])
        data_cube[f] /= data_med
        hdulist.close()

    # get median
    log.write("Merging....")
    bias_data = np.float32(np.median(data_cube, axis=0))

    # generate fits structure and save to new file
    new_hdulist = fits.HDUList()
    pri_hdu = fits.PrimaryHDU(header=hdulist[0].header)
    #pri_hdu.header.append(("FLATCNT", n_file, "Bias files count used in this merge"))
    #pri_hdu.header.append(("FLATDATE", now_str(), "Flat process time"))
    pri_hdu.header.update(FLATCNT=(n_file, "Bias files count used in this merge"),
                          FLATDATE=(now_str(), "Flat process time"))
    new_hdulist.append( pri_hdu )
    for a in range(const.n_amp) :
        img_hdu = fits.ImageHDU(data=bias_data[a], header=hdulist[a + 1].header)
        new_hdulist.append( img_hdu )

    log.write("Save flat to `{:s}`".format(out_flat_file))
    new_hdulist.writeto(out_flat_file)

    log.close()
