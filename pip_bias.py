#!/usr/bin/env python
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


if __name__ == "__main__" :
    a = {"tel":None, "list":None, "bias":None, "prefix":"",
         "base":"", "debug":5, "overwrite":False}
    alias = {"arg_01":"tel", "arg_02":"list", "arg_03":"bias"}
    a = args.arg_trans(sys.argv, a, alias=alias, silent=True)
    if a["tel"] is None :
        print ("""This is a shell caller for pipeline.
Syntax: 
    ./pip_bias.py [tel=]tel [list=]listfile [bias=]biasfile [prefix=prefix]
        [base=basedir] [debug=debug] [overwrite=true|false]
Arguments:
    tel: telescope name, now we have bok and xao
    list: a named argument, value is path and filename of list file
    bias: a named argument, value is path and filename of output bias file
    prefix: a prefix add to list and bias, this makes calling short
    base: a optional named argument, base directory add to filenames in list
    debug: debug info display level, for leveles, see manual, default is 5
    overwrite: a named optional bool argument, true or false
Example:
    ./pip_bias.py bok list=/data/red/bok/u/201608/J7606/list/bias.lst
                      bias=/data/red/bok/u/201608/J7606/bias.fits
    ./pip_bias.py bok list/bias.lst bias.fits prefix=/data/red/bok/u/201608/J7606/
Note:
    If prefix is applied, make sure the use of slash(/) is correct
        """)
    else :
        if a["tel"].lower() == "bok" :
            import bok as tel
        elif a["tel"].lower() == "xao" :
            import xao as tel
        else :
            print ("Unknown telescope `{tel}`".format(tel=a["tel"]))

        global debug
        debug = a["debug"]
        print ("Merge bias: "
               "\n\tlist file  ={list}"
               "\n\toutput bias={bias}"
               "\n\tbase dir   ={base}"
               "\n\tdebug level={debug}"
               "".format(
            list=a["prefix"]+a["list"], bias=a["prefix"]+a["bias"], base=a["base"], debug=debug))
        tel.merge_bias(a["prefix"]+a["list"], a["prefix"]+a["bias"],
                       a["base"], overwrite=a["overwrite"])


