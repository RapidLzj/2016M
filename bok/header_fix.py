# -*- coding: utf-8 -*-
"""
    2016-06-18, 2016M-1.0 lzj
    Load header from fits, and fix fields
    For bok
"""


import numpy as np
from astropy.io import fits
from common import *
from .constant import const


def header_fix (raw_fits) :
    """ Load adn fix fits header
    args:
        raw_fits: file filename
    returns:
        tuple of fits header, and info object
        fits header object, error fixed, and append necessary fields
    """
    # get primary header, and header of ext 1, which has wcs info
    hdr0 = fits.getheader(raw_fits, 0)
    hdr1 = fits.getheader(raw_fits, 1)

    # basic info from primary header, and process special case
    ob = sxpar(hdr0, "OBJECT", "UNKNOWN")
    fn = raw_fits
    fs = fn[-9:-5]
    fi = sxpar(hdr0, "FILTER")
    ut = sxpar(hdr0, "UT")
    et = sxpar(hdr0, "EXPTIME")

    if ob[0] == """ : ob = ob[1:].strip()
    if ob[-1] == """ : ob = ob[:-1].strip()
    if ob == "" : ob = "unknown"

    if fs.isdigit() :
        fs = int(fs)
    else :
        fs = -1

    # copy info from hdr1 to hdr0
    hdr0.update(EQUINOX=(sxpar(hdr1, "EQUINOX")),
        WCSDIM=(sxpar(hdr1, "WCSDIM")),
        CTYPE1=(sxpar(hdr1, "CTYPE1")),
        CTYPE2=(sxpar(hdr1, "CTYPE2")),
        CRVAL1=(sxpar(hdr1, "CRVAL1")),
        CRVAL2=(sxpar(hdr1, "CRVAL2")),
        CRPIX1=(sxpar(hdr1, "CRPIX1")),
        CRPIX2=(sxpar(hdr1, "CRPIX2")),
        CD1_1 =(sxpar(hdr1, "CD1_1" )),
        CD1_2 =(sxpar(hdr1, "CD1_2" )),
        CD2_1 =(sxpar(hdr1, "CD2_1" )),
        CD2_2 =(sxpar(hdr1, "CD2_2" )) )
    # other info
    hdr0.update(EPOCH   = 2000.0,
                RADECSYS= "FK5",
                CROTA1  = 0.0,
                CROTA2  = 0.0,
                CUNIT1  = "deg",
                CUNIT2  = "deg")
    # keep old ra / dec
    hdr0.update(OLD_RA  =(sxpar(hdr0, "RA"    ), "Old Right Ascension"),
                OLD_DEC =(sxpar(hdr0, "DEC"   ), "Old Declination"),
                OLD_CRV1=(sxpar(hdr0, "CRVAL1"), "Old Reference Value 1 (Dec)"),
                OLD_CRV2=(sxpar(hdr0, "CRVAL2"), "Old Reference Value 2 (RA)"))

    # site info and observation date and time, from header
    #site_ele = sxpar(hdr0, "SITEELEV") * 1.0
    #site_lat = hms2dec(sxpar(hdr0, "SITELAT"))
    #site_lon = hms2dec(sxpar(hdr0, "SITELONG")) * (-1.0)
    date_obs = sxpar(hdr0, "DATE-OBS")
    time_obs = sxpar(hdr0, "TIME-OBS")
    objra    = sxpar(hdr0, "CRVAL2")
    objdec   = sxpar(hdr0, "CRVAL1")
    mjd = sky.mjd(int(date_obs[0:4]), int(date_obs[5:7]), int(date_obs[8:10]),
                  int(time_obs[0:2]), int(time_obs[3:5]), float(time_obs[6:12]))
    lst = sky.lst(mjd, const.site_lon)
    #jd = julday(strmid(date_obs, 5, 2), strmid(date_obs, 8, 2), strmid(date_obs, 0, 4), $
    #strmid(time_obs, 0, 2), strmid(time_obs, 3, 2), strmid(time_obs, 6, 6))
    # calc moon phase / ra / dec, transfer to moon azimuth / altitud
    # (MPHASE RA_MOON DEC_MOON MAZIMUTH MALTITUD)
    mp = sky.moon_pos(mjd)
    mph = sky.moon_phase(mjd) * 100.0
    maz, malt = sky.azalt(const.site_lat, lst, mp.ra, mp.dec)
    #moonpos, jd, mra, mdec
    #mphase, jd, mph
    #eq2hor, mra, mdec, jd, malt, maz, mha, lat = site_alt, lon = site_lon, alt = site_ele
    # calc moon - object angle(MANGLE)
    ma = sky.distance(mp.ra, mp.dec, objra, objdec)
    #ma = map_2points(mra, mdec, objra, objdec)
    #ma = ma[0]
    hdr0.update(MPHASE  =(mph,    "Moon phase (percent)"),
                RA_MOON =(mp.ra,  "RA of Moon (degree)"),
                DEC_MOON=(mp.dec, "Dec of Moon (degree)"),
                MAZIMUTH=(maz,    "Azimuth of Moon (degree)"),
                MALTITUD=(malt,   "Altitude of Moon (degree)"),
                MANGLE  =(ma,     "Angle from Moon to Object (degree)"))
    # object Alt and Az, HA(write AZMTHANG ELEANG HA AIRMASS)
    #eq2hor, objra, objdec, jd, objalt, objaz, objha, lat = site_alt, lon = site_lon, alt = site_ele
    #airmass = 1.0 / sin((objalt + 244.0 / (165.0 + 47.0 * objalt ^ 1.1)) * !pi / 180.d)
    objaz, objalt = sky.azalt(const.site_lat, lst, objra, objdec)
    airm = sky.airmass(const.site_lat, lst, objra, objdec)
    objha = sky.hourangle(lst, objra)
    hdr0.update(AZIMUTH=(objaz,  "Object Azimuth"),
                ELEVAT =(objalt, "Object Altitude"),
                HA     =(objha,  "Object Hour angle"),
                AIRMASS=(airm,   "Airmass"))

    hdr0.update(BZERO=0.0)

    gain = [0.0] * const.n_amp
    for a in range(const.n_amp) :
        gain[a] = sxpar(hdr0, "GAIN"+const.amp_strp[a])

    hinfo = info("Image_Header",
        object=ob,
        filename=fn,
        filesn=fs,
        flt=fi,
        utc=ut,
        expt=et,
        mjd=mjd,
        objra=objra,
        objdec=objdec,
        gain=gain)

    return hdr0, hinfo
