#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 08:24:09 2018

@author: jur
"""
import pickle

def sock_send_df(sock, df):
    for ix, row in df.iterrows():
        sock.send(pickle.dumps(row.to_dict()))
