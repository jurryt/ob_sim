#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 20:19:39 2018

@author: jur
"""
from settings import BEHAVIOUR, S, MIN_D, MAX_X, MAX_Y
from utils import dist, rnd_vec


#class SimpleBot:
    
#    def __init__(self, radius=5.0):
#        self.radius = radius
        
def set_df(df):
    s = (df['machine_type']==__name__.split('.')[-1])
    
    col_x_trg, col_y_trg = 'x_trg', 'y_trg'                

#    df.loc[s,'x_near'] = df.loc[s,'x_trg']
#    df.loc[s,'y_near'] = df.loc[s,'y_trg']
    for ix, row in df.loc[s].iterrows():
        #print(i,r)
        neighbour_ix = dist(row.x,row.y,df[df.index!=ix].x,df[df.index!=ix].y).idxmin()
        # if I am not the nearest set nearest as target
#        if ix!=neighbour_ix:
        df.loc[ix,'x_near'] = df.loc[neighbour_ix,'x']
        df.loc[ix,'y_near'] = df.loc[neighbour_ix,'y']
   
    # reward
    df.loc[s,'ds'] = dist(df.loc[s,'x'], df.loc[s,'y'], df.loc[s,col_x_trg], df.loc[s,col_y_trg])
    df.loc[s,'dx'] = df.loc[s,col_x_trg] - df.loc[s,'x']
    df.loc[s,'dy'] = df.loc[s,col_y_trg] - df.loc[s,'y']

    # penalty
    df.loc[s,'ds1'] = dist(df.loc[s,'x'], df.loc[s,'y'], df.loc[s,'x_near'], df.loc[s,'y_near'])
    df.loc[s,'dx1'] = -(df.loc[s,'x_near'] - df.loc[s,'x'])
    df.loc[s,'dy1'] = -(df.loc[s,'y_near'] - df.loc[s,'y'])

   
    # speed is max(the remaining dist, S) ds is always positive
    selection = s & (df['ds']>0)
    #if not selection.empty:
    fr = df.loc[selection]
    df.loc[selection,'u'] = fr.ds.clip_upper(S) * fr['dx']/fr['ds']
    df.loc[selection,'v'] = fr.ds.clip_upper(S) * fr['dy']/fr['ds']

    df.loc[selection,'u1'] = fr.ds.clip_upper(S) * fr['dx1']/fr['ds1']
    df.loc[selection,'v1'] = fr.ds.clip_upper(S) * fr['dy1']/fr['ds1']

    df.loc[selection,'u'] += df.loc[selection,'u1']
    df.loc[selection,'v'] += df.loc[selection,'v1']
    
    # on collision turn left
    selection = s & (df['collision'])
    u = df.loc[selection, 'v']
    v = -df.loc[selection, 'u']
    df.loc[selection, 'u'] = u
    df.loc[selection, 'v'] = v

    # determine if target is reached and set new target
    # new target should come from blockchain
    selection = s & (df['ds'].abs()<MIN_D)
    #if not selection.empty:
    l = len(df.loc[selection])
    if l>0:
        print('targets reached', l)
    df.loc[selection,'x_trg'] = rnd_vec(l,MAX_X)
    df.loc[selection, 'y_trg'] = rnd_vec(l,MAX_Y)

        
        
        