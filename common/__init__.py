#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    This is version 2016M of pipeline for sage sky survey.
    Rewrite using python, original version using IDL
    This package is for common usage among different telescopes

    Author: Jie ZHENG: jiezheng@nao.cas.cn
    Version: 2016M (M for 2nd half of June)
    Location: Steward Observatory, University of Arizona, Tucson, AZ
"""


from util import *
from progress_bar import *
from logger import *
from msg_box import *
from info import *
import angle
import sky
import cata
