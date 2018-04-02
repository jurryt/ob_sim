#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 07:14:08 2018

@author: jur
"""

N = 10#100#3#10
MAX_X = 100
MAX_Y = 100

S = 1.0#.1#2 # fixed speed
MIN_D = 1e-4 # precision / minimal measurable distance
R=100#200#00 # nr of runs

#BEHAVIOUR = 'nearest_target'
#BEHAVIOUR = 'solo'
BEHAVIOUR = 'gradient'

MOVIE = True #False|True
INTERPOLATION = 'cubic'#'linear' or 'nearest'

HOST = 'localhost'
PORT = 10000