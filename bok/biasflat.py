"""
    2016-06-16, 2016M-1.0 lzj
    Bias and flat merge
    For bok
"""

import numpy as np
from astropy.io import fits
from rm_os import rm_os
from common.util import *
import os, time


def merge_bias(bias_list, out_bias_file , basedir='', debug=0):
    """ Merge bias with median values
    args:
        bias_list: bias file list or list file
        out_bias_file: output filename
        basedir: path added to files in list
        debug: debug level
    returns:
        1 if ok, 0 or -1 for error
    """

    (files, n_file) = common.list_expand(bias_list, basedir=basedir, debug=debug)
    if not is_list_exists(files, debug=debug) :
        raise IOError('Not all files in list exist')

    nx, ny = 2048, 2016
    namp = 16
    data_cube = np.empty([n_file, namp, nx, ny], dtype=np.float32)

    # load data into cube, overscan removed
    for f in range(n_file) :
        if debug >= 2 : print ('#%3d/%3d Loading: %s' % (f+1, n_file, files[f]))
        hdulist = fits.open(files[f])
        for a in range(namp) :
            data_cube[f, a] = rm_os(hdulist[a+1].data)
        hdulist.close()

    # get median
    if debug >= 2: print ('Merging....')
    bias_data = np.median(data_cube, axis=0)

    # generate fits structure and save to new file
    nowstr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    new_hdulist = fits.HDUList()
    pri_hdu = fits.PrimaryHDU(header=hdulist[0].header)
    pri_hdu.header.append(('BIASCNT', n_file, 'Bias files count used in this merge'))
    pri_hdu.header.append(('BIASDATE', nowstr, 'Bias process time'))
    new_hdulist.append( pri_hdu )
    for a in range(namp) :
        img_hdu = fits.ImageHDU(data=bias_data[a], header=hdulist[a+1].header)
        new_hdulist.append( img_hdu )

    print ('Save bias to %s' % (out_bias_file))
    new_hdulist.writeto(out_bias_file)


def merge_flat ( flat_list, bias_file, out_flat_file, basedir='', debug=0 ) :
    """Merge flat with normalized median values
    :param flat_list: flat file list or list file
    :param bias_file: bias fits file
    :param out_flat_file: output filename
    :param basedir: path added to files in list
    :param debug: debug level
    :returns: 1 if ok, 0 or -1 for error
    """

    (files, n_file) = list_expand(flat_list, basedir=basedir, debug=debug)
    if not is_list_exists(files, debug=debug):
        raise IOError('Not all files in list exist')
    if not os.path.isfile(bias_file) :
        raise IOError('bias file not exist')

    nx, ny = 2048, 2016
    namp = 16
    data_cube = np.empty([n_file, namp, nx, ny], dtype=np.float32)

    biashdu = fits.open(bias_file)

    # load data into cube, overscan removed
    for f in range(n_file) :
        if debug >= 2: print ('#%3d/%3d Loading: %s' % (f+1, n_file, files[f]))
        hdulist = fits.open(files[f])
        for a in range(namp) :
            # remove overscan and bias
            data_one = rm_os(hdulist[a+1].data) - biashdu[a+1].data
            # normalize
            data_med = np.median(data_one)
            data_cube[f, a] = data_one / data_med
        hdulist.close()

    # get median
    if debug >= 2: print ('Merging....')
    bias_data = np.median(data_cube, axis=0)

    # generate fits structure and save to new file
    nowstr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    new_hdulist = fits.HDUList()
    pri_hdu = fits.PrimaryHDU(header=hdulist[0].header)
    pri_hdu.header.append(('FLATCNT', n_file, 'Bias files count used in this merge'))
    pri_hdu.header.append(('FLATDATE', nowstr, 'Bias process time'))
    new_hdulist.append( pri_hdu )
    for a in range(namp) :
        img_hdu = fits.ImageHDU(data=bias_data[a], header=hdulist[a+1].header)
        new_hdulist.append( img_hdu )

    print (u'Save flat to {0:s}'.format(out_flat_file))
    new_hdulist.writeto(out_flat_file)
