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
    
def rnd_vec(n, mx):
    return np.random.rand(n)*mx

def dist(x0, y0, x1, y1):
    return ((x1-x0)**2 + (y1-y0)**2)**0.5

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
    
class World:

    def __init__(self, N = 50, MAX_X = 100, MAX_Y = 100, 
                 S = .1, MIN_D = 1e-4, R=200, BEHAVIOUR = 'gradient',
                 MOVIE = True, INTERPOLATION = 'cubic'):
        
        #BEHAVIOUR = 'nearest_target'
        #BEHAVIOUR = 'solo'
        self.N = N
        self.MAX_X = X
        self.MAX_Y = Y
        self.S = S
         #False|True
        #'linear' or 'nearest'
        
        # part of robots
        print(BEHAVIOUR)

        # initialize the world
        self.df = pd.DataFrame(index=range(N), 
                          data={'x': rnd_vec(N,MAX_X),
                                'y': rnd_vec(N,MAX_Y)})

        # robot
        # initialize rest target positions and velocities
        self.df['x_trg'] = rnd_vec(N,MAX_X)
        self.df['y_trg'] = rnd_vec(N,MAX_Y)

        # TODO reference frame, z and w
        self.df['u'] = 0     # speed in x direction (TODO: reference frome)
        self.df['v'] = 0     # speed in y direction (TODO: reference frome)
        
        #df['id'] = df.index
        # ?
        k=''


        self.fig, self.ax = plt.subplots(figsize=(10,7))
        #ax = fig.add_axes([0,0,MAX_X,MAX_Y], frameon=False)
        self.ax.set_xlim(0, MAX_X)
        self.ax.set_ylim(0, MAX_Y)
        #ax.axis([0,0,MAX_X,MAX_Y])
        self.scat = self.ax.scatter(x=self.df['x'],y=self.df['y'], marker='o')#, animated=True)
        self.scat_trg = ax.scatter(x=self.df['x_trg'],y=df['y_trg'], marker='+')#, animated=True)
        
        
        
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
        
                
            
            
#       following does not work only one label please (complex nrs could work in 2D :-)        
#        pd.merge_asof(df,df[['x','y']],left_on=['x_trg','y_trg'], right_on=['x','y'], direction='nearest', suffixes=('','_waypoint'))
        
    
    # speed is max(the remaining dist, S)
    selection = df['ds']>0
    fr = df.loc[selection]
    df.loc[selection,'u'] = fr.ds.clip_upper(S) * fr['dx']/fr['ds']
    df.loc[selection,'v'] = fr.ds.clip_upper(S) * fr['dy']/fr['ds']
    
    df['x'] = df['x'] + df['u']
    df['y'] = df['y'] + df['v']
    


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


    # target reached ?
    selection = df['ds'].abs()<MIN_D
    l = len(df.loc[selection])
    df.loc[selection,'x_trg'] = rnd_vec(l,MAX_X)
    df.loc[selection, 'y_trg'] = rnd_vec(l,MAX_Y)
    dfs.append(df.copy())
    
    return scat, scat_trg, contour
        
#        k = input()
#while True:
#    loop(0)
ani = anim.FuncAnimation(fig,update,frames=R,  repeat=False, interval=500)
#plt.show()
if MOVIE:
    ani.save(BEHAVIOUR+'.mp4')
    
ani3d = anim.FuncAnimation(fig3d,update,frames=R,  repeat=False, interval=500)

if MOVIE:
    ani3d.save(BEHAVIOUR+'3D.mp4')
    
result = pd.concat(dfs)
    