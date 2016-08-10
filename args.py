# -*- coding: utf-8 -*-
"""
    This is version 2016M of pipeline for sage sky survey.
    Rewrite using python, original version using IDL
    This file is for commandline arguments process.

    Author: Jie ZHENG: jiezheng@nao.cas.cn
    Version: 2016M (M for 2nd half of June)
    Location: Steward Observatory, University of Arizona, Tucson, AZ
"""


def arg_trans (argv, default=None, restrict=True, silent=False):
    """ A function reduce commandline arguments.
        Recognize them into two categories: arguments by order and by name.
        Directly arguments will be taken as ordered arguments, will be entitled as ARG01, ARG02, etc.
        Arguments like key=value will taken as named arguments, reuse its own name.
        The default key=value dict will provide missing arguments.
        If restrict is true, only names in default is valid, other names will be abandoned.
        Note: NOT use ARGxx as keyword for named arguments.
    args:
        argv: argument values from `sys.argv`
        default: providing default key-value dict
        restrict: bool, restrict names in default or not. If default is None, this will not effect.
        silent: display error message or not
    returns:
        dict of these arguments
    """
    if default is None :
        res = {}
        restrict = False  # if default is None, this argument is meaningless
    else :
        res = default.copy()

    arg_cnt = 0
    for a in argv :
        kv = a.split("=")
        if len(kv) == 1 :
            k = "arg_{:02d}".format(arg_cnt)
            arg_cnt += 1
            v = kv[0]
        else :
            k = kv[0]
            v = kv[1]
            if v == "" : v = True
        if not restrict or k in res :
            res[k] = v
        else :
            if not silent : print ("Argument `{}` NOT recognized.".format(k))

    for k in res :
        if res[k] is None :
            if not silent : print ("Argument `{}` required but missing.".format(k))

    return res

