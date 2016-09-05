#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    2016-09-04, 2016M-1.0 lzj
    Pipeline shell for all steps
    For bok
"""


from . import *



def pipeline (raw_path, red_path, bare_fits,
              skip_bf=False, skip_phot=False, skip_wcs=False, skip_mag=False,
              bias_file=None, flat_file=None,
              keep=True, sex_cmd="sextractor",
              aper_rad=None, do_psf=False,
              wcs_catalog=None, wcs_match_distan=0.002, recenter=False,
              mag_catalog="catalog/HM1998", match_mode=1, mag_match_distan=0.002,
              ver_from=None, ver_to=None, overwrite=False
              ) :
    """ A pipeline caller for all steps
    All arguments comes from steps
    skip_xx: a bool flag decide do or not do a step
    """

    stepflag = ( 0 if skip_bf else 1<<3 +
                 0 if skip_phot else 1<<2 +
                 0 if skip_wcs else 1<<1 +
                 0 if skip_mag else 1<<0 )
    # 0 0000 x   1 0001 v   2 0010 v   3 0011 v
    # 4 0100 v   5 0101 x   6 0110 v   7 0111 v
    # 8 1000 v   9 1001 x  10 1010 x  11 1011 x
    #12 1100 v  13 1101 x  14 1110 v  15 1111 v
    if stepflag in (0, 5, 9, 10, 11, 13) :
        print ("Steps skip policy is invalid. Abort!")
        return -1

    if not skip_bf :
        bfcorrect(raw_path=raw_path, red_path=red_path, bare_fits=bare_fits,
                  bias_file=bias_file, flat_file=flat_file,
                  ver_to=ver_to, overwrite=overwrite)
        ver_from = ver_to

    if not skip_phot :
        photomerey(raw_path=raw_path, red_path=red_path, bare_fits=bare_fits,
                   keep=keep, sex_cmd=sex_cmd,
                   aper_rad=aper_rad, do_psf=do_psf,
                   ver_from=ver_from, ver_to=ver_to, overwrite=overwrite)
        ver_from = ver_to

    if not skip_wcs :
        astromerey(red_path=red_path, bare_fits=bare_fits,
                   wcs_catalog=wcs_catalog, wcs_match_distan=wcs_match_distan, recenter=recenter,
                   ver_from=ver_from, ver_to=ver_to, overwrite=overwrite)
        ver_from = ver_to

    if not skip_mag :
        magcalibrate(red_path=red_path, bare_fits=bare_fits,
                     mag_catalog=mag_catalog, match_mode=match_mode, mag_match_distan=mag_match_distan,
                     ver_from=ver_from, ver_to=ver_to, overwrite=overwrite)
        ver_from=ver_to

    report(red_path=red_path, bare_fits=bare_fits, ver_from=ver_from, overwrite=overwrite)

