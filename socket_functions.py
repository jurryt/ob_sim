#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 08:24:09 2018

@author: jur
"""
import pickle

print_ConnectionRefusedError = True

def sock_send_df(sock, df):
    global print_ConnectionRefusedError
    for ix, row in df[df['blender_name']!=''].iterrows():
        try:
            sock.send(pickle.dumps(row.to_dict()))
        except ConnectionRefusedError as exp:
            if print_ConnectionRefusedError:
                print(exp)
                print_ConnectionRefusedError = False
            break
        
        
def sock_send_grid(sock, _id, x, y, z):
    global print_ConnectionRefusedError
    d = {'blender_type': 'grid'}
    d['x'] = x.tolist()
    d['y'] = y.tolist()
    d['z'] = z.tolist()
    try:
        sock.send(pickle.dumps(d))
    except ConnectionRefusedError as exp:
        if print_ConnectionRefusedError:
            print(exp)
            print_ConnectionRefusedError = False
    
