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
    a = args.arg_trans(sys.argv[1:], {"arg_01":None, "list":None, "bias":None, "prefix":"", "base":""})
    if a["atg_01"] is None :
        print ("""Syntax: ./pip_bias.py tel list=listfilename bias=biasfilename [prefix=prefix] [base=basedir]
        tel: telescope name, now we have bok and xao
        list: a named argument, value is path and filename of list file
        bias: a named argument, value is path and filename of output bias file
        root: a prefix add to list and bias, this makes calling short
        base: a optional named argument, base directory add to filenames in list
    Example:
        ./pip_bias.py bok list=/data/red/bok/u/201608/J7601/list/bias.lst bias=/data/red/bok/u/201608/J7601/bias.fits
        ./pip_bias.py bok prefix=/data/red/bok/u/201608/J7601/ list=list/bias.lst bias=bias.fits
    Notiice:
        If prefix is applied, make sure the use of slash(/) is correct
        """)
    elif a["arg_01"] == "bok" :
        print ("Merge bias: \n\tlist file={list}\n\toutput bias={bias}\n\tbase dir={base}".format(
            list=a["base"]+a["list"], bias=a["base"]+a["bias"], base=a["base"]))
        bok.merge_bias(a["base"]+a["list"], a["base"]+a["bias"], a["base"])
    elif a["arg_01"] == "xao" :
        #xao.merge_bias(a["base"] + a["list"], a["base"] + a["bias"], a["base"])
        print ("Sorry, xao pipeline is not ready now.")
    else :
        print ("Telescope `{}` NOT recognized.")