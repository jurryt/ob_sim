#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 06:45:16 2018

@author: jur
"""
from time import sleep

from pymongo import MongoClient
import pandas as pd

from database import db_read_df, db_update_df
from utils import rnd_vec, dist
from settings import N, MAX_X, MAX_Y, BEHAVIOUR, MIN_D, S

#%%
# setup database
client = MongoClient()
db = client.world

# set initial target and speed
df = db_read_df(db)
# initialize rest target positions and velocities
df['x_trg'] = rnd_vec(N,MAX_X)
df['y_trg'] = rnd_vec(N,MAX_Y)

# TODO reference frame, z and w
df['u'] = 0     # speed in x direction (TODO: reference frome)
df['v'] = 0     # speed in y direction (TODO: reference frome)

db_update_df(db, df)

while True:
    # get positions
    df = db_read_df(db)
    

    if BEHAVIOUR == 'solo':
        # calc distance velocities x_target - x
        #df['ds'] = dist(df['x'], df['y'], df['x_trg'], df['y_trg'])
        #df['dx'] = df['x_trg'] - df['x']
        #df['dy'] = df['y_trg'] - df['y']
        col_x_trg, col_y_trg = 'x_trg', 'y_trg'                

    elif BEHAVIOUR == 'nearest_target':
        # we travel via the robot nearest to target if any
        # for default we take original target
        df['x_near'] = df['x_trg']
        df['y_near'] = df['y_trg']
        for ix, row in df.iterrows():
            #print(i,r)
            neighbour_ix = dist(row.x_trg,row.y_trg,df.x,df.y).idxmin()
            # if I am not the nearest set nearest as target
            if ix!=neighbour_ix:
                df.loc[ix,'x_near'] = df.loc[neighbour_ix,'x']
                df.loc[ix,'y_near'] = df.loc[neighbour_ix,'y']
        
        col_x_trg, col_y_trg = 'x_near', 'y_near'
    elif BEHAVIOUR == 'gradient':
        #utility = fn_cost(utility, df)
        #fn_cost(df)                
        # dummy                
        col_x_trg, col_y_trg = 'x_trg', 'y_trg'                

    else:
        raise NotImplemented
        
    df['ds'] = dist(df['x'], df['y'], df[col_x_trg], df[col_y_trg])
    df['dx'] = df[col_x_trg] - df['x']
    df['dy'] = df[col_y_trg] - df['y']
   
    # speed is max(the remaining dist, S)
    selection = df['ds']>0
    fr = df.loc[selection]
    df.loc[selection,'u'] = fr.ds.clip_upper(S) * fr['dx']/fr['ds']
    df.loc[selection,'v'] = fr.ds.clip_upper(S) * fr['dy']/fr['ds']

    # determine if target is reached and set new target
    selection = df['ds'].abs()<MIN_D
    l = len(df.loc[selection])
    df.loc[selection,'x_trg'] = rnd_vec(l,MAX_X)
    df.loc[selection, 'y_trg'] = rnd_vec(l,MAX_Y)

    db_update_df(db,df)
    
#    print(df.head(1))
    #sleep(1)