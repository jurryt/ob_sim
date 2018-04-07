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
#import socket

#from socket_functions import sock_send_df, sock_send_grid

#alex
from bigchaindb_driver.crypto import generate_keypair
#alex end


import asyncio
#import datetime
import random
import websockets
#import json
from machine_types import simplebot
machine_modules = (simplebot,)


#def fn_cost(df, method='nearest'):
#    # http://scipy-cookbook.readthedocs.io/items/Matplotlib_Gridding_irregularly_spaced_data.html
##    x,y = 
#    
#    for ix, row in df.iterrows():
#        fr=df[df.index!=ix]
#        df.loc[ix,'cost'] = -sum((1/dist(row.x,row.y,fr.x,fr.y)))
#
#    xi=np.linspace(0,MAX_X)
#    yi=np.linspace(0,MAX_Y)
#    
#    zi = griddata((df.x.values, df.y.values), 
#                  df.cost.values, 
#                  (xi[None,:],yi[:,None]), 
#                  method=method,
#                  fill_value=0.0)
#    
#    return xi, yi, zi

def cost_function(df, selection, machine_id, method='nearest'):
    
#        df.loc[s,'x_near'] = df.loc[s,'x_trg']
#        df.loc[s,'y_near'] = df.loc[s,'y_trg']
    
        
#    for ix, row in fr.iterrows():
        #print(i,r)
        
#        df.loc[selection,'neighbour'] = dist(row.x,row.y,fr[fr.index!=ix].x,fr[fr.index!=ix].y).idxmin()
        # if I am not the nearest set nearest as target
#        if ix!=neighbour_ix:
#            df.loc[ix,'x_near'] = df.loc[neighbour_ix,'x']
#            df.loc[ix,'y_near'] = df.loc[neighbour_ix,'y']
        
        #col_x_trg, col_y_trg = 'x_near', 'y_near'

    
    
    # do only one point
    #for ix, row in df.loc[selection].iterrows():
        #fr=df[df.index!=ix]
   #     df.loc[ix,'cost'] = 1#-sum((1/dist(row.x,row.y,fr.x,fr.y)))

    if 'ix_near' in df.columns:

        neighbour_id = df.loc[machine_id,'ix_near']

        df.loc[int(neighbour_id),'cost'] = 1.0


    xi=np.linspace(0,MAX_X)
    yi=np.linspace(0,MAX_Y)
    
    
    fr= df.loc[selection]
    reward = np.zeros(len(fr))
    
    reward[machine_id]=-1.0
    
    
    zi = griddata((np.array([*fr.x.values, *fr.x_trg.values]), np.array([*fr.y.values, *fr.y_trg.values])), 
                  np.array([*fr.cost.values, *reward]),
                  (xi[None,:],yi[:,None]), 
                  method=method,
                  fill_value=0.0)
    
    return xi, yi, zi
    
#async def send_data(websocket, path):
#def main():
# setup database

def world_gen()    :

    client = MongoClient()
    db = client.world    
    
    #    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #    sock.connect((HOST, PORT))
    
    print(BEHAVIOUR)
    
    #%%
    db_clear(db)
    df = pd.DataFrame(index=range(N), 
                      data={'x': rnd_vec(N,MAX_X),
                            'y': rnd_vec(N,MAX_Y)})
    
    # alex      
    df['private_key'] = 'empty' # bigchaindb private key for each unique robot
    df['public_key'] = 'empty' # bigchaindb public key for each unique robot
    df['state'] = 'empty' # intial state of the robot. this state is later stored in metadata tag in blockchaindb 
    for ix, row in df.iterrows():
        current_keypair = generate_keypair()
        private_key = current_keypair.private_key     
        public_key = current_keypair.public_key     
        df.loc[ix,'private_key'] = private_key
        df.loc[ix,'public_key'] = public_key
    # alex end
        
    # blender specific columns
    df['blender_name'] = ''
    df['blender_type'] = 'object'
    df.loc[0,'blender_name'] = 'car.001'
    
    #df.loc[:N/2,'machine_type'] = 'simplebot'
    df['machine_type'] = 'simplebot'
    df['radius'] = 0.5
    df['collision'] = False
    df['cost'] = 0.0
    #df['u']=0.0
    #df['v']=0.0
    
    df['x_trg'] = rnd_vec(N,MAX_X)
    df['y_trg'] = rnd_vec(N,MAX_Y)
        
    db_update_df(db, df)
    
    #xi, yi, zi=fn_cost(df, method=INTERPOLATION)
    #xi, yi, zi=cost_function(df, 0, method=INTERPOLATION)
    #db_update_grid(db, 'world', xi, yi, zi)
    
    while True:
        
        # read machines information 
        # get rid of nans
        df = db_read_df(db)
        
        for machine_module in machine_modules:
            machine_module.set_df(df)
        
        
        # velocity has been set by machines
        if 'u' in df.columns and 'v' in df.columns:
            
            selection = ~df.u.isna() & ~df.v.isna()
            
            df.loc[selection, 'x_new'] = df.loc[selection, 'x'] + df.loc[selection, 'u']
            df.loc[selection, 'y_new'] = df.loc[selection, 'y'] + df.loc[selection, 'v']
            
            for ix, row in df.iterrows():
                fr=df[df.index!=ix]
                df.loc[ix,'collision'] = any(dist(row.x_new,row.y_new,fr.x_new,fr.y_new)<=(fr.radius+row.radius))
            
            collisions = len(df[df.collision])
            if collisions>0:
                print('collisions', collisions)
            
            df.loc[~df.collision,'x'] = df.loc[~df.collision,'x_new']
            df.loc[~df.collision,'y'] = df.loc[~df.collision,'y_new']
            
            db_update_df(db, df.loc[selection])
        
        #xi, yi, zi=fn_cost(df, method=INTERPOLATION)
            # only if we have a target
            xi, yi, zi=cost_function(df,selection, 0, method=INTERPOLATION)
        
            db_update_grid(db, 'world', xi, yi, zi)
        
            grid = {'world':{'x':xi,'y':yi,'z':zi}}
        
        yield df, grid

if __name__ == '__main__':
    for df, grid in world_gen():
        pass

    
#            sock_send_grid(sock, 'world', xi, yi, zi)
        
#        sock_send_df(sock, df)
    #await websocket.send(df.to_json(orient='records'))
    #await asyncio.sleep(random.random() * 3)

#main()
#start_server = websockets.serve(send_data, '0.0.0.0', 5678)

#asyncio.get_event_loop().run_until_complete(start_server)
#asyncio.get_event_loop().run_forever()
