#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 07:14:08 2018

@author: jur
"""
SETTINGS ={
    'N' : 2,#100#100#3#10
    'MAX_X' : 60,#-20#60
    'MAX_Y' : 30,#-20#30
    'S' : 1,#.1#1.0#0.1#1.0#.1#2 # fixed speed
    'MIN_D' : 1e-4, # precision / minimal measurable distance
    'INTERPOLATION' : 'linear', #'cubic'#'linear' or 'nearest'  
    'R' :100,#200#00 # nr of runs

    'USE_BIGCHAINDB' : True,

#BEHAVIOUR = 'nearest_target'
#BEHAVIOUR = 'solo'
#BEHAVIOUR = 'gradient'

    'MOVIE' : False, #False|True
    
    'machines':{'simplebot':{'speed':1.0,'reward':1.0,'penalty':1.0}}
    

        }

#INTERPOLATION = 'nearest'

HOST = 'localhost'
#HOST = '10.1.2.15'
PORT = 10000

# alex
# initialize object which all robots will use to communicate to the 
# global DB. These setttings are derived from the test server so 
# for each user registration this is different (set the app_id and app_key)
# you need to register on boghchaindb and get this information under
# "connect in python", which you can find on https://testnet.bigchaindb.com/

tokens = {}
#alex
#tokens['app_id'] = '4a33bc96'
#tokens['app_key'] = '5e9699fbe0c5bca83d35e3a7e63ba1c1'
#jur
tokens['app_id'] = 'dbd40a9c'
tokens['app_key'] = 'a8062ad9546eba03f4f61ad7f6d4afac'
from bigchaindb_driver.crypto import generate_keypair
master_keys = generate_keypair()

# alex end
