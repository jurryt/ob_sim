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

from settings import HOST, PORT
import socket

from socket_functions import sock_send_df, sock_send_grid


import asyncio
#import datetime
import websockets
#import json

from world import world_gen
    
async def send_data(websocket, path):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((HOST, PORT))
    
    for df, grid in world_gen():
        #sock_send_grid(sock, 'world', grid['world']['x'], grid['world']['y'], grid['world']['z'])
        sock_send_grid(sock, df)
            
        sock_send_df(sock, df)
        await websocket.send(df.to_json(orient='records'))
        #await asyncio.sleep(random.random() * 3)


start_server = websockets.serve(send_data, '0.0.0.0', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
