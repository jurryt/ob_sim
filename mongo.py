#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 20:31:02 2018

@author: jur
"""

from pymongo import MongoClient

class Machines:
    
    def __init__(self, db, init):
        self.db = db
        self.positions = self.db.positions
        for _id, position in init.items():
            self.positions.update_one({'_id': _id},
                                      {'$set': position},
                                      upsert=True)
            





client = MongoClient()
db = client.test_database

init={0:{'x':1.0,'y':2.0}, 1: {'x':2.0,'y':4.0}}
#init = {}

machines = Machines(db,init)


#positions = db.positions
#pos_id = positions.insert_one({'x':1.0,'y':2.0}).inserted_id