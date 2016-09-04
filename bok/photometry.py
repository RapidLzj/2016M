#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    2016-06-18, 2016M-1.0 lzj
    Call SExrtactor to do extract source from seperated fits,
    and merge frame result
    For bok
"""


import numpy as np
from astropy.io import fits
import photutils
from common import *
from .constant import const
from .header_fix import header_fix


def photomerey(raw_path, red_path, bare_fits,
               keep=True, sex_cmd="sextractor",
               aper_rad=None, do_psf=False,
               ver_from=None, ver_to=None, overwrite=False):
    """ Call SExrtactor to do extract source from separated fits, and merge
    argument:
        raw_path: path of raw fits file
        red_path: path of output science path
        bare_fits: fits file without path and extension
        keep: keep bf corrected fits after sex, default false
        sex_cmd: sex command, different system may differ, default sextractor
        aper_rad: aperture photon count radii array
        do_psf: if set, do psf photometry
        ver_from: version which data come from
        ver_to: version which data write to
        overwrite: is set, overwrite existing output files
    return:
        n_star if OK, -1 if error
    """
    # argument check
    # process global debug level
    global debug
    if "debug" not in globals() :
        debug = 0
    # version prefix
    ver_from = "" if ver_from is None or ver_from == "" else "." + ver_from
    ver_to = "" if ver_to is None or ver_to == "" else "." + ver_to
    # path end check
    if not raw_path.endswith("/") : raw_path += "/"
    if not red_path.endswith("/") : red_path += "/"
    prefix_from = red_path + bare_fits + ver_from + "."
    prefix_to = red_path + bare_fits + ver_to + "."

    log = logger(prefix_to + "phot.log", "Photometry", debug)

    # filenames
    raw_fits = raw_path + bare_fits + "fits"
    in_fits = [prefix_from + a + ".fits" for a in const.amp_str]
    outs_ldac = [prefix_to + a + "s.ldac" for a in const.amp_str] # output of sex
    phots_ldac = prefix_to + "phots.ldac" # whole catalog from sex
    phots_cat = prefix_to + "phots.cat"
    photi_ldac = prefix_to + "photi.ldac" # whole catalog from iraf like method
    photi_cat = prefix_to + "photi.cat"
    psf_def = prefix_to + "psf.def"

    if not file_exist([in_fits, raw_fits], log) :
        log.write("File missing. Abort!", -1)
        return -1
    if not overwrite_check(overwrite, [outs_ldac, phots_ldac, phots_cat, photi_ldac, photi_cat], log) :
        log.write("Output files exist without overwrite flag. Abort!", -1)
        return -1

    # load raw header and fix fields, extract some fields into object
    hdr, hinfo = header_fix(raw_fits)

    # data about each amp
    sky_med = np.zeros(const.n_amp, dtype=np.float32)
    sky_std = np.zeros(const.n_amp, dtype=np.float32)
    sky_mag = np.zeros(const.n_amp, dtype=np.float32)
    sky_err = np.zeros(const.n_amp, dtype=np.float32)
    img_amp = np.empty([const.n_amp, const.amp_ny, const.amp_nx], dtype=np.float32)
    cata_amp = []
    n_star_amp = []

    # process each piece
    for a in range(const.n_amp) :
        # call sex, and load result, store in a super list
        cmd = "{sex} {fits} -c lzj.sex -CATALOG_NAME {ldac} -GAIN {gain:5.3f} -PIXEL_SCALE {ps:6.3f}".format(
            sex=sex_cmd, fits=in_fits[a], ldac=outs_ldac[a], gain=hinfo.gain[a], ps=const.pix_scales)
        os.system(cmd)
        cata = fits.getdata(outs_ldac[a], 2)
        cata_amp.append(cata)
        n_star_amp.append(len(cata))
        # estimate mean fwhm of image
        fwhm = np.median(cata_amp["fwhm_image"])
        # load image
        img = fits.getdata(in_fits[a])
        img_amp[a, :, :] = img
        # do background estimate for image, median+-sigma, and then to mag+-err
        # do circle aper photometry on sex found stars, and make a new table to contain data

        # using iraf find find objects in image, and then do aper
        # generate a new table
        # rotate catalog and merge into big table

    # save merged table as new catalog





    log.close()
