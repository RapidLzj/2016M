#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    This is version 2016M of pipeline for sage sky survey.
    Rewrite using python, original version using IDL
    This package is for Bok telescope data reduction, most part are specified for bok.

    Author: Jie ZHENG: jiezheng@nao.cas.cn
    Version: 2016M (M for 2nd half of June)
    Location: Steward Observatory, University of Arizona, Tucson, AZ
"""


from .rm_os import rm_os
from .merge_bias import merge_bias
from .merge_flat import merge_flat
from .bfcorrect import bfcorrect
from .photometry import photomerey
from .astrometry import astromerey
from .report import report

