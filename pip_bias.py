#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    This is version 2016M of pipeline for sage sky survey.
    Rewrite using python, original version using IDL
    This file is a shell caller for merge_bias.

    Author: Jie ZHENG: jiezheng@nao.cas.cn
    Version: 2016M (M for 2nd half of June)
    Location: Steward Observatory, University of Arizona, Tucson, AZ
"""


import sys
import args
import bok


if __name__ == "__main__" :
    a = args.arg_trans(sys.argv, {"arg_01":None, "list":None, "bias":None, "prefix":"", "base":"", "debug":5, "overwrite":False}, silent=True)
    if a["arg_01"] is None :
        print ("""This is a shell caller for pipeline.
Syntax: 
    ./pip_bias.py tel list=listfilename bias=biasfilename [prefix=prefix] [base=basedir] [overwrite=]
        tel: telescope name, now we have bok and xao
        list: a named argument, value is path and filename of list file
        bias: a named argument, value is path and filename of output bias file
        root: a prefix add to list and bias, this makes calling short
        base: a optional named argument, base directory add to filenames in list
        debug: debug info display level, for leveles, see manual
        overwrite: a named optional bool argument, nothing at right of =
Example:
    ./pip_bias.py bok list=/data/red/bok/u/201608/J7601/list/bias.lst bias=/data/red/bok/u/201608/J7601/bias.fits
    ./pip_bias.py bok prefix=/data/red/bok/u/201608/J7601/ list=list/bias.lst bias=bias.fits
Notiice:
    If prefix is applied, make sure the use of slash(/) is correct
        """)
    elif a["arg_01"] == "bok" :
        debug = a["debug"]
        print ("Merge bias: \n\tlist file  ={list}\n\toutput bias={bias}\n\tbase dir   ={base}\n\tdebug level={debug}".format(
            list=a["prefix"]+a["list"], bias=a["prefix"]+a["bias"], base=a["base"], debug=debug))
        bok.merge_bias(a["prefix"]+a["list"], a["prefix"]+a["bias"], a["base"], overwrite=a["overwrite"])

    elif a["arg_01"] == "xao" :
        debug = a["debug"]
        print ("Merge bias: \n\tlist file  ={list}\n\toutput bias={bias}\n\tbase dir   ={base}\n\tdebug level={debug}".format(
            list=a["prefix"]+a["list"], bias=a["prefix"]+a["bias"], base=a["base"], debug=debug))
        #xao.merge_bias(a["prefix"]+a["list"], a["prefix"]+a["bias"], a["base"], overwrite=a["overwrite"])
        print ("Sorry, xao pipeline is not ready now.")

    else :
        print ("Telescope `{}` NOT recognized.")

