# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 12:27:15 2018

@author: PietersmaJ

TODO: 
    1. add gradient field 
    2. turn into server 
    3. add 3djs visualization 
    4. collisions 
    5. reference frame
    6.....

"""
import numpy as np
import pandas as pd 

from scipy.interpolate import griddata

from pymongo import MongoClient
from database import db_read_df, db_update_df, db_clear, db_update_grid,db_read_grid
from settings import N, MAX_X, MAX_Y, BEHAVIOUR, INTERPOLATION, HOST, PORT
from utils import rnd_vec, dist
import socket

from socket_functions import sock_send_df, sock_send_grid

def fn_cost(df, method='nearest'):
    # http://scipy-cookbook.readthedocs.io/items/Matplotlib_Gridding_irregularly_spaced_data.html
#    x,y = 
    
    for ix, row in df.iterrows():
        fr=df[df.index!=ix]
        df.loc[ix,'cost'] = -sum((1/dist(row.x,row.y,fr.x,fr.y)))

    xi=np.linspace(0,MAX_X)
    yi=np.linspace(0,MAX_Y)
    
    zi = griddata((df.x.values, df.y.values), 
                  df.cost.values, 
                  (xi[None,:],yi[:,None]), 
                  method=method)#,
                  #fill_value=0)
    
    return xi, yi, zi
    
# setup database
client = MongoClient()
db = client.world    

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect((HOST, PORT))

print(BEHAVIOUR)

#%%
db_clear(db)
df = pd.DataFrame(index=range(N), 
                  data={'x': rnd_vec(N,MAX_X),
                        'y': rnd_vec(N,MAX_Y)})
    
df['blender_name'] = ''
df['blender_type'] = 'object'

df.loc[0,'blender_name'] = 'car.001'
    
db_update_df(db, df)

xi, yi, zi=fn_cost(df, method=INTERPOLATION)
db_update_grid(db, 'world', xi, yi, zi)

while True:
    
    # read machines information 
    df = db_read_df(db)
    
    # velocity has been set by machines
    if 'u' in df.columns and 'v' in df.columns:
        df['x'] = df['x'] + df['u']
        df['y'] = df['y'] + df['v']
        db_update_df(db, df)

    xi, yi, zi=fn_cost(df, method=INTERPOLATION)
    
    db_update_grid(db, 'world', xi, yi, zi)
    
    sock_send_df(sock, df)
    sock_send_grid(sock, 'world', xi, yi, zi)
    
