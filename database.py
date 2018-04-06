#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 06:59:03 2018

@author: jur
"""
import pandas as pd
import numpy as np

def db_clear(db):
    machines = db.machines
    machines.remove()
    grids = db.grids
    grids.remove()

def db_replace_df(db, df):
    machines = db.machines
    for ix, row in df.iterrows():
        machines.replace_one({'_id': int(ix)},
                                   row.to_dict(),
                                   upsert=True)


def db_update_df(db, df):
    machines = db.machines
    for ix, row in df.iterrows():
        machines.update_one({'_id': int(ix)},
                                   {'$set': row.to_dict()},
                                   upsert=True)

def db_update_grid(db, _id, x, y, z):
    grids = db.grids
    grids.update_one(
            {'_id': _id},
            {'$set': {'x':x.tolist(),'y':y.tolist(),'z':z.tolist()}}, 
            upsert=True)


def db_read_df(db):
    machines = db.machines
    rows=[]
    for row in machines.find():
        rows.append(row)
    
    df=pd.DataFrame(rows)
    df.set_index('_id', inplace=True)
    
    return df

def db_read_grid(db, _id):
    grids = db.grids    
    grid_dict = grids.find_one({'_id':_id})
    x = np.array(grid_dict['x'])
    y = np.array(grid_dict['y'])
    z = np.array(np.array(grid_dict['z']))
    return x,y,z