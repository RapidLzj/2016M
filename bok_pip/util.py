"""
    2016-06-17, 2016M-1.0 lzj
    Utilities for pipeline, general operations
    For bok
"""


import os


def list_expand ( alist , basedir='', debug=0 ):
    """Expand list if given a filename. remove all comments and empty lines
    alist   : list or filename
    basedir : optional, if given, add to filename
    debug   : debug info level, default 0
    :returns: list of filenames
    """
    if isinstance(alist, str) :
        if debug >= 9 :
            print ('Expand list file %s' % alist)
        if os.path.isfile(alist) :
            with open(alist, 'r') as fp :
                xlist = fp.readlines()
        else :
            raise IOError('file %s NOT exists.' % alist)
    else :
        xlist = alist

    fs = [basedir + line.strip() for line in xlist
            if not line.strip().startswith('#') and line.strip() != '']

    nf = len(fs)
    return (fs, nf)


def is_list_exists ( alist, basedir='', debug=0 ) :
    """Check all file in list exists
    alist   : list of files to check, will be expanded
    basedir : optional, add to head of filename
    debug   : debug level, default 0
    :returns: true if all files exists, false else
    """

    (files, n_file) = list_expand(alist, basedir)

    check = [os.path.isfile(afile) for afile in files]
    if debug >= 9 :
        for i in range(n_file):
            print ('%5s %s' % (check[i], files[i]))

    return all(check)

