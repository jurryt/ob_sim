#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 07:14:08 2018

@author: jur
"""

N = 50#100#100#3#10
MAX_X = 60#-20#60
MAX_Y = 30#-20#30

S = .5#1.0#0.1#1.0#.1#2 # fixed speed
MIN_D = 1e-4 # precision / minimal measurable distance
R=100#200#00 # nr of runs

#BEHAVIOUR = 'nearest_target'
#BEHAVIOUR = 'solo'
BEHAVIOUR = 'gradient'

MOVIE = False #False|True
#INTERPOLATION = 'cubic'#'linear' or 'nearest'
INTERPOLATION = 'linear'

HOST = 'localhost'
PORT = 10000