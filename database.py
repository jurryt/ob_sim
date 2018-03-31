#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 06:59:03 2018

@author: jur
"""
import pandas as pd

def db_clear(db):
    machines = db.machines
    machines.remove()

def db_replace_df(db, df):
    machines = db.machines
    for ix, row in df.iterrows():
        machines.replace_one({'_id': ix},
                                   row.to_dict(),
                                   upsert=True)


def db_update_df(db, df):
    machines = db.machines
    for ix, row in df.iterrows():
        machines.update_one({'_id': ix},
                                   {'$set': row.to_dict()},
                                   upsert=True)

def db_read_df(db):
    machines = db.machines
    rows=[]
    for row in machines.find():
        rows.append(row)
    
    df=pd.DataFrame(rows)
    df.set_index('_id')
    
    return df
