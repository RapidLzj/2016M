#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    2016-06-17, 2016M-1.0 lzj
    Bias and flat correction for original fits, and separate into simple fits by amp
    For bok
"""


import numpy as np
from astropy.io import fits
from rm_os import rm_os
from common import *
from constant import const


def bfcorrect (raw_path, red_path, bare_fits, bias_file, flat_file,
               ver_to=None) :
    """ Correct data fits with bias and flat
    argument:
        raw_path: path of raw fits file
        red_path: path of output science path
        bare_fits: fits file without path and extension
        flat_file: flat fits filename, full name with path and ext
        bias_file: bias fits filename, full name
    returns:
        0 if ok, other for error
    """
    # argument check
    # process global debug level
    global debug
    if "debug" not in globals():
        debug = 0
    # version prefix
    ver_from = "" # just make things looks like
    ver_to = "" if ver_to is None or ver_to == "" else "." + ver_to
    # path end check
    if not raw_path.endswith("/") : raw_path += "/"
    if not red_path.endswith("/") : red_path += "/"
    prefix_from = raw_path+bare_fits + ver_from + "."
    prefix_to = red_path+bare_fits + ver_to + "."

    log = logger(prefix_to + "bf.log", "BiasFlatCorrect", debug)

    raw_fits = prefix_from + "fits"
    out_fits = [prefix_to + a + ".fits" for a in const.amp_str]

    # check file exists
    if not os.path.isfile(bias_file):
        raise IOError("Bias file `{}` NOT EXIST.".format(bias_file))
    if not os.path.isfile(flat_file):
        raise IOError("Flat file `{}` NOT EXIST.".format(flat_file))
    if not os.path.isfile(raw_fits):
        raise IOError("Raw data fits `{}` file NOT EXIST.".format(raw_fits))

    raw_hdu = fits.open(raw_fits)
    bias_hdu = fits.open(bias_file)
    flat_hdu = fits.open(flat_file)

    pri_hdu = fits.PrimaryHDU()
    for a in range(const.n_amp) :
        data = (rm_os(raw_hdu[a + 1].data, log) - bias_hdu[a + 1].data) / flat_hdu[a + 1].data
        pri_hdu.data = data
        pri_hdu.header = raw_hdu[a + 1].header
        pri_hdu.header.extent(raw_hdu[0].header.cards)
        pri_hdu.writeto(out_fits[a])

    log.write("Bias and flat corrected for {}".format(bare_fits))

    log.close()

