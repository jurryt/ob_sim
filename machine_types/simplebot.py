#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 20:19:39 2018

@author: jur
"""
from settings import BEHAVIOUR, S, MIN_D, MAX_X, MAX_Y, tokens,master_keys
from utils import dist, rnd_vec
# alex - needs to be in bigchaindb
from bigchaindb_driver import BigchainDB
from time import sleep
# alex end 

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
    reward = 1.0
    df.loc[s,'ds'] = reward * dist(df.loc[s,'x'], df.loc[s,'y'], df.loc[s,col_x_trg], df.loc[s,col_y_trg])
    df.loc[s,'dx'] = df.loc[s,col_x_trg] - df.loc[s,'x']
    df.loc[s,'dy'] = df.loc[s,col_y_trg] - df.loc[s,'y']

    # penalty
    penalty = 1.0#1.0
    df.loc[s,'ds1'] = penalty * dist(df.loc[s,'x'], df.loc[s,'y'], df.loc[s,'x_near'], df.loc[s,'y_near'])
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

     # TODO: doesn't really work
#    df.loc[selection,'u'] += df.loc[selection,'u1']
#    df.loc[selection,'v'] += df.loc[selection,'v1']
    
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

# alex
# this code uses simple binary state change to describe whether the robot is carrying
# an asset (for example energy or a parcel or whatever)    
    for ix, row in df.loc[selection].iterrows(): # for each bot that reached a new waypoint change its behaviour
        if df.loc[ix,'state'] == 'empty':
            print('empty bot changed to carry')
            df.loc[ix,'state'] = 'carry'
            #create 
            bdb = BigchainDB('https://test.bigchaindb.com', headers=tokens)
            parcel_asset = {
                'data': {
                    'parcel': {
                        'serial_number': '9999',
                        'manufacturer': 'producer'
                    },
                },
            }

            parcel_asset_metadata = {
                'parceltype': 'box'
            }            
            tx1 = bdb.transactions.prepare(
            operation='CREATE',
                signers=master_keys.public_key,
                recipients=master_keys.public_key,
                asset=parcel_asset,
                metadata=parcel_asset_metadata
            )
            print('Transaction 1', tx1)
            tx_signed1 = bdb.transactions.fulfill(
                tx1,
                private_keys=master_keys.private_key
            )
            sent_creation_tx = bdb.transactions.send(tx_signed1)
            txid = tx_signed1['id']
            trials = 0
            while trials < 60:
                try:
                    if bdb.transactions.status(txid).get('status') == 'valid':
                        print('Tx Create valid in:', trials, 'secs')
                        break
                except:
                    trials += 1
                    sleep(1)
            if trials == 60:
                print('Tx is still being processed... Bye!')
                exit(0)                                    
        if df.loc[ix,'state'] == 'carry':
            print('carry bot changed to empty')
            df.loc[ix,'state'] = 'empty'
# alex end                
        
        