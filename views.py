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
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from mpl_toolkits.mplot3d import Axes3D

from scipy.interpolate import griddata

from pymongo import MongoClient
from database import db_read_df, db_update_df, db_clear, db_update_grid,db_read_grid
from settings import N, MAX_X, MAX_Y, R, BEHAVIOUR, MOVIE, INTERPOLATION
from utils import rnd_vec, dist


    
# setup database
client = MongoClient()
db = client.world    


df = db_read_df(db)
xi, yi, zi = db_read_grid(db, 'world')
# plotting
# scatter plot
fig, ax = plt.subplots(figsize=(10,7))
ax.set_xlim(0, MAX_X)
ax.set_ylim(0, MAX_Y)
scat = ax.scatter(x=df['x'],y=df['y'], marker='o')#, animated=True)
scat_trg = ax.scatter(x=[],y=[],marker='+')#, animated=True)
# contour
contour = ax.contour(xi, yi, zi)#, levels=np.linspace(0,1,num=10))
# mesh
fig3d = plt.figure(figsize=(10,7))
ax3d = fig3d.add_subplot(111,projection='3d')
xm,ym = np.meshgrid(xi,yi)
ax3d.plot_wireframe(xm,ym,zi)

#while k=='':
def update(frame_number):
#    for r in range(R):

#    for x in range(MAX_X):
#        for 
#    distance_grid = zeros(MAX_X, )
    global contour #, utility
    
    # read machines information 
    df = db_read_df(db)
    xi, yi, zi = db_read_grid(db, 'world')
    
    # velocity has been set by machines
    if 'x_trg' in df.columns and 'y_trg' in df.columns:

        scat.set_offsets(df[['x','y']].values)
        scat_trg.set_offsets(df[['x_trg','y_trg']].values)
#    contour.set_array(utility)
    #scat.set_offsets(np.concatenate([df[['x','y']].values,df[['x_trg','y_trg']].values]))
    for c in contour.collections:
        c.remove()
#    contour = ax.contour(utility,levels=np.linspace(0,1,num=10))
#    contour = ax.contour(df.x,df.y,df.cost, levels=np.linspace(0,1,num=10))
#    contour = ax.contour(df[['x','y','cost']])#, levels=np.linspace(0,1,num=10))
 #   fr=df.pivot('x','y','cost').fillna(0) 
 #   xc,yc=np.meshgrid(fr.index,fr.columns)
 #   contour = ax.contour(xc,yc,fr.values)#, levels=np.linspace(0,1,num=10))
    
    xm,ym = np.meshgrid(xi,yi)
#xc,yc=np.meshgrid(fr.index,fr.columns)
    contour = ax.contour(xi, yi, zi)#, leve

    for c in ax3d.collections:
        c.remove()

    ax3d.plot_wireframe(xm,ym,zi)

    
    return scat, scat_trg, contour
        
#        k = input()
#while True:
#    loop(0)
ani = anim.FuncAnimation(fig,update,frames=R,  repeat=True, interval=500)
#plt.show()
if MOVIE:
    ani.save(BEHAVIOUR+'.mp4')
    
ani3d = anim.FuncAnimation(fig3d,update,frames=R,  repeat=True, interval=500)

if MOVIE:
    ani3d.save(BEHAVIOUR+'3D.mp4')
    
#result = pd.concat(dfs)
    