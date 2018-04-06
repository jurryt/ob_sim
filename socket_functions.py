#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 08:24:09 2018

@author: jur
"""
#import pickle
from send_json import send_json
import json

print_ConnectionRefusedError = True

def sock_send_df(sock, df):
    global print_ConnectionRefusedError
#    for ix, row in df[df['machine_type']!='simplebot'].iterrows():
    for ix, row in df.iterrows():
        try:
            #sock.send(pickle.dumps(row.to_dict()))
            d = {
                  "mode": "change_scene",
                   "car."+str(int(ix)+1).zfill(3): {
                    "type": "car",
                    "loc": {
                      "y": row.y,
                      "z": 0.0,
                      "x": row.x,
                    },
                    "rot": {
                      "y": 0.0,
                      "z": 0.0,
                      "x": 0.0
                    },
                    "vel": {
                        "u": row.u,
                        "v": row.v,
                            },
                    "other":
                        {
                        "x_trg":row.x_trg,        
                        "y_trg": row.y_trg,
                        "radius": row.radius
                        }
                   }
                }
            send_json(json.dumps(d), sock)
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
    
