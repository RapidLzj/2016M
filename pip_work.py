#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This is version 2016M of pipeline for sage sky survey.
    Rewrite using python, original version using IDL
    This file is a shell caller for pipeline.

    Author: Jie ZHENG: jiezheng@nao.cas.cn
    Version: 2016M (M for 2nd half of June)
    Location: Steward Observatory, University of Arizona, Tucson, AZ
"""


import sys
import args


if __name__ == "__main__" :
    ar = {"tel":None, "raw_path":"", "red_path":"", "bare_fits":"",
          "skip_bf":False, "skip_phot":False, "skip_wcs":False, "skip_mag":False,
          "bias_file":"", "flat_file":"",
          "keep":True, "sex_cmd":"sextractor",
          "aper_rad":"", "do_psf":False,
          "wcs_catalog":None, "wcs_match_distan":0.002, "recenter":False,
          "mag_catalog":"catalog/HM1998", "match_mode":1, "mag_match_distan":0.002,
          "ver_from":"", "ver_to":"", "overwrite":False, "debug":5}
    alias = {"arg_01":"tel", "arg_02":"raw_path", "arg_03":"red_path", "arg_04":"bare_fits"}

    ar = args.arg_trans(sys.argv, ar, alias=alias, silent=True)
    if ar["tel"] is None :
        print ("""This is a shell caller for pipeline.
Syntax:
    ./pip_work.py [tel=]tel ......
        """)
    else :
        if ar["tel"].lower() == "bok" :
            import bok as tel
        elif ar["tel"].lower() == "xao" :
            import xao as tel
        else :
            print ("Unknown telescope `{tel}`".format(tel=ar["tel"]))

        global debug
        debug = ar["debug"]

        print ("Call pipeline:")
        for k in ar :
            print ("{k} = {v}".format(k=k, v=ar[k]))

        tel.pipeline(raw_path=ar["raw_path"],
                     red_path=ar["red_path"],
                     bare_fits=ar["bare_fits"],
                     skip_bf=ar["skip_bf"],
                     skip_phot=ar["skip_phot"],
                     skip_wcs=ar["skip_wcs"],
                     skip_mag=ar["skip_mag"],
                     bias_file=ar["bias_file"],
                     flat_file=ar["flat_file"],
                     keep=ar["keep"],
                     sex_cmd=ar["sex_cmd"],
                     aper_rad=ar["aper_rad"],
                     do_psf=ar["do_psf"],
                     wcs_catalog=ar["wcs_catalog"],
                     wcs_match_distan=ar["wcs_match_distan"],
                     recenter=ar["recenter"],
                     mag_catalog=ar["mag_catalog"],
                     match_mode=ar["match_mode"],
                     mag_match_distan=ar["mag_match_distan"],
                     ver_from=ar["ver_from"],
                     ver_to=ar["ver_to"],
                     overwrite=ar["overwrite"]
        )
