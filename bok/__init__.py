"""
    This is version 2016M of pipeline for sage sky survey.
    Rewrite using python, original version using IDL
    This package is for Bok telescope data reduction, most part are specified for bok.

    Author: Jie ZHENG: jiezheng@nao.cas.cn
    Version: 2016M (M for 2nd half of June)
    Location: Steward Observatory, University of Arizona, Tucson, AZ
"""

from rm_os import *
from biasflat import *
from photometry import *
from astrometry import *
from report import *

# debug level code
# -1: silent mode, only display 'Done' after task finished, and display critical error
#  0: normal mode, display some running info
#  1: currently same as 0, for future use
#  2: display detailed process info
#  3-7: same as 2
#  8: debug mode, but no base level info
#  9: debug mode, all debug info from all level
