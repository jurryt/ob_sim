#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 07:15:28 2018

@author: jur
"""
import numpy as np

def rnd_vec(n, mx):
    return np.random.rand(n)*mx


def dist(x0, y0, x1, y1):
    return ((x1-x0)**2 + (y1-y0)**2)**0.5

