# -*- coding: utf-8 -*-
"""
    2016-06-17, 2016M-1.0 lzj
    Utilities for pipeline, general operations
    This part including file and list operations
"""


import os
import time


def list_expand (alist , basedir='', log=None):
    """ Expand list if given a filename. remove all comments and empty lines
    args:
        alist   : list or filename
        basedir : optional, if given, add to filename
        debug   : debug info level, default 0
    returns:
        list of filenames
    """
    if isinstance(alist, str) :
        log.write("Expand list file `{}`".format(alist), 9)
        if os.path.isfile(alist) :
            with open(alist, "r") as fp :
                xlist = fp.readlines()
        else :
            raise IOError("file `{}` NOT exists.".format(alist))
    else :
        xlist = alist

    fs = [basedir + line.strip() for line in xlist
            if not line.strip().startswith("#") and line.strip() != ""]

    nf = len(fs)
    return (fs, nf)


def is_list_exists (alist, basedir="", log=None) :
    """ Check all file in list exists
    args:
        alist   : list of files to check, will be expanded
        basedir : optional, add to head of filename
        debug   : debug level, default 0
    returns:
        true if all files exists, false else
    """
    (files, n_file) = list_expand(alist, basedir)

    check = [os.path.isfile(afile) for afile in files]
    for i in range(n_file):
        log.write("{:5} {}".format(check[i], files[i]), 9)

    return all(check)


def overwrite_check (overwrite, files, log=None) :
    """ Check existance of output files, and the overwrite flag
    args:
        overwrite: bool, overwrite or not
        files: full name of output files to check
        log: logger
    returns:
        True if OK, not exists, or have overwrite flag. False if any file exists and overwrite is not set.
    """
    res = True
    for f in files :
        if os.path.isfile(f) :
            if overwrite :
                log.write("<{}> exists, and will be overwrited".format(f), 1)
            else :
                log.write("<{}> exists.".format(f), -1)
                res = False
    return res


def read_file (filename, default=None) :
    """ Read configure file, and remove comments, empty lines
    args:
        filename: configure file name
        default: default content if file not exists
    returns:
        a list of lines, leading and tailing space striped, empty line and comment removed
    """
    if os.path.isfile(filename) :
        lines = open(filename, "r").readlines()
    else :
        lines = default

    outlines = []
    for l in lines :
        k = l.split("#")[0].strip()
        if k != "" :
            outlines.append(k)

    return outlines


def now_str() :
    """ Get formatted current UTC time : yyyy-mm-dd hh:mm:ss """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())


def sxpar (header, key, default=None) :
    """ Check weather the key is in header, if yes, return value, else return default
    args:
        header: fits head, get from hdulist[x].header
        key: key of the card you want to visit
        default: default value if key not in header, and if key exists, but value is empty
    returns:
        value of key, if not exists or empty, return default value
    """
    if key in header.keys() :
        v = header[key]
        if v == "" :
            v = default
        if type(v) == str :
            v = v.strip()
    else :
        v = default
    return v
