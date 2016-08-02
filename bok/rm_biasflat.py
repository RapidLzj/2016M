"""
    2016-06-17, 2016M-1.0 lzj
    Bias and flat correction for original fits, and seperate into simple fits by amp
    For bok
"""


import numpy as np
from astropy.io import fits
from rm_os import rm_os
from common.util import *
import os, time


def rm_biasflat (raw_path, sci_path, bare_fits, flat_file, bias_file, debug=0) :
    """ Correct data fits with bias and flat
    argument:
        raw_path: path of raw fits file
        sci_path: path of output science path
        bare_fits: fits file without path and extention
        flat_file: flat fits filename, full name with path and ext
        bias_file: bias fits filename, full name
        debug: debug level
    returns:
        0 if ok, other for error
    """

    nx, ny = 2048, 2016
    namp = 16
    ampcode = ["%2.2d" % a for a in range(1, 17)]

    if not raw_path.endswith("/") : raw_path += "/"
    if not sci_path.endswith("/"): sci_path += "/"

    raw_fits = raw_path+bare_fits+".fits"
    out_fits = [sci_path+bare_fits+"."+a+".fits" for a in ampcode]

    # check file exists
    if not os.path.isfile(bias_file):
        raise IOError('Bias file not exist')
    if not os.path.isfile(flat_file):
        raise IOError('Flat file not exist')
    if not os.path.isfile(raw_fits):
        raise IOError('Raw data fits file not exist')

    raw_hdu = fits.open(raw_fits)
    bias_hdu = fits.open(bias_file)
    flat_hdu = fits.open(flat_file)

    pri_hdu = fits.PrimaryHDU()
    for a in range(namp) :
        data = (rm_os(raw_hdu[a+1].data, debug=debug) - bias_hdu[a+1].data) / flat_hdu[a+1].data
        pri_hdu.data = data
        pri_hdu.header = raw_hdu[a+1].header
        pri_hdu.header.extent(raw_hdu[0].header.cards)
        pri_hdu.writeto(out_fits[a])

    print ("Bias and flat corrected for %s" % (bare_fits))