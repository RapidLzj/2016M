# -*- coding: utf-8 -*-
"""
    2016-06-17, 2016M-1.0 lzj
    Constants for pipeline, general operations
    This part providing some constants, necessary for pipeline, but difference between telescopes.
"""


class const (object) :
    """ A static class, providing constants
    """
    # amp number and names
    n_amp = 16
    amp_str = ["{:02d}".format(t + 1) for t in range(n_amp)] # names with leading 0: 01-16
    amp_strp = ["{:d}".format(t + 1) for t in range(n_amp)]  # names without leading 0: 1-16

    # x/y const of image piece
    gap_x, gap_y  = 119, 364    # gap width (height) in center of whole image
    amp_nx, amp_ny = 2016, 2048 # size of each amp
    amp_nx_os = 2036            # overscan size
    amp_ctx, amp_cty = amp_nx / 2 - 0.5 , amp_ny / 2 - 0.5      # center x/y for each amp
    amp_rot = [2, 7, 5, 0, 2, 7, 5, 0, 0, 5, 7, 2, 0, 5, 7, 2]  # rotate parameter for each amp

    # x/y start of each amp in whole image
    amp_xt = [1, 0, 1, 0, 3, 2, 3, 2, 0, 1, 0, 1, 2, 3, 2, 3]
    amp_yt = [1, 1, 0, 0, 1, 1, 0, 0, 2, 2, 3, 3, 2, 2, 3, 3]
    amp_x0 = [amp_nx * t if t < 2 else amp_nx * t + gap_x for t in amp_xt]
    amp_y0 = [amp_ny * t if t < 2 else amp_ny * t + gap_y for t in amp_yt]

    # whole image
    ctx, cty = 4091.04 - 1, 4277.99 - 1 # center
    fov = 1.0                           # field of view in degrees
    pix_scales = 0.445                  # arcseconds for each pixel
    pix_scaled = pix_scales / 3600.0    # in degrees
    pix_scales2 = pix_scales ** 2       # pixel area to squared arcsecond
    rot_ang = 0.0                       # rotate angle of whole image

    # Site Info
    site_lon = - (111 + 36 / 60.0 + 01.6 / 3600.0) # longitude
    site_lat = 31 + 57 / 60.0 +  46.5 / 3600.0     # latitude
    site_ele = 2071.0                              # elevation
    site_tz  = -7                                  # timezone, MST

    # record structure of catalog : [(name, type, unit, disp)]
    cols = [("starno",    "J", "No",  "5d"),
            ("mjd",       "I", "DAY", "04d"),
            ("fileno",    "I", "NO",  "04d"),
            ("filter",    "8A","",    "8s"),
            ("x",         "E", "PIX", "10.5f"),
            ("y",         "E", "PIX", "10.5f"),
            ("elong",     "E", "",    "5.3f"),
            ("fwhm",      "E", "PIX", "6.3f"),
            ("mag_auto",  "E", "MAG", "6.3f"),
            ("err_auto",  "E", "MAG", "6.4f"),
            ("mag_best",  "E", "MAG", "6.3f"),
            ("err_best",  "E", "MAG", "6.4f"),
            ("mag_petro", "E", "MAG", "6.3f"),
            ("err_petro", "E", "MAG", "6.4f"),
            ("mag_aper1", "E", "MAG", "6.3f"),
            ("err_aper1", "E", "MAG", "6.4f"),
            ("mag_aper2", "E", "MAG", "6.3f"),
            ("err_aper2", "E", "MAG", "6.4f"),
            ("mag_aper3", "E", "MAG", "6.3f"),
            ("err_aper3", "E", "MAG", "6.4f"),
            ("mag_aper4", "E", "MAG", "6.3f"),
            ("err_aper4", "E", "MAG", "6.4f"),
            ("mag_aper5", "E", "MAG", "6.3f"),
            ("err_aper5", "E", "MAG", "6.4f"),
            ("flags",     "B", "",    "8b"),
            ("mag_corr",  "E", "MAG", "6.3f"),
            ("err_corr",  "E", "MAG", "6.4f"),
            ("radeg",     "D", "DEG", "10.6f"),
            ("decdeg",    "D", "DEG", "10.6f"),
            ("raerr",     "E", "SEC", "5.2f"),
            ("decerr",    "E", "SEC", "5.2f"),
            ("rastr",     "11A","HMS","11s"),
            ("decstr",    "11A","DMS","11s"),
            ("ixwcs",     "J",  "NO", "5d"),
            ("ixmag",     "J",  "NO", "5d"),
            ("ampno",     "B",  "NO", "2d"),
            ]
