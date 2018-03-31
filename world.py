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
from database import db_read_df, db_update_df, db_replace_df, db_clear
from settings import N, MAX_X, MAX_Y, R, BEHAVIOUR, MOVIE, INTERPOLATION
from utils import rnd_vec, dist


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


print(BEHAVIOUR)

#%%
df = pd.DataFrame(index=range(N), 
                  data={'x': rnd_vec(N,MAX_X),
                        'y': rnd_vec(N,MAX_Y)})

db_clear(db)
db_replace_df(db, df)
#%%
#df['id'] = df.index

k=''


fig, ax = plt.subplots(figsize=(10,7))
#ax = fig.add_axes([0,0,MAX_X,MAX_Y], frameon=False)
ax.set_xlim(0, MAX_X)
ax.set_ylim(0, MAX_Y)
#ax.axis([0,0,MAX_X,MAX_Y])
scat = ax.scatter(x=df['x'],y=df['y'], marker='o')#, animated=True)
#scat_trg = ax.scatter(x=df['x_trg'],y=df['y_trg'], marker='+')#, animated=True)
scat_trg = ax.scatter(x=[],y=[],marker='+')#, animated=True)


#utility = np.zeros((MAX_X,MAX_Y))
#f#n_cost(utility, df)
xi, yi, zi=fn_cost(df, method=INTERPOLATION)
#fr=df.pivot('x','y','cost').fillna(0)
#xc,yc=np.meshgrid(fr.index,fr.columns)
contour = ax.contour(xi, yi, zi)#, levels=np.linspace(0,1,num=10))

fig3d = plt.figure(figsize=(10,7))
ax3d = fig3d.add_subplot(111,projection='3d')

xm,ym = np.meshgrid(xi,yi)

ax3d.plot_wireframe(xm,ym,zi)


dfs=[df.copy()]
#while k=='':
def update(frame_number):
#    for r in range(R):

#    for x in range(MAX_X):
#        for 
#    distance_grid = zeros(MAX_X, )
    global contour , utility
    
    # read machines information 
    df = db_read_df(db)
    
    # velocity has been set by machines
    if 'u' in df.columns and 'v' in df.columns:
    
        
        df['x'] = df['x'] + df['u']
        df['y'] = df['y'] + df['v']
        
        db_update_df(db, df)

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
    xi, yi, zi=fn_cost(df, method=INTERPOLATION)
    
    xm,ym = np.meshgrid(xi,yi)



    
#fr=df.pivot('x','y','cost').fillna(0)
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
    
result = pd.concat(dfs)
    