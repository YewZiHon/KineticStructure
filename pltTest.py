import time

import matplotlib.pyplot as plt
import numpy as np
import json

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
np.set_printoptions(precision=2)

# Make the X, Y meshgrid.
xs = np.linspace(1, 12, 12)
ys = np.linspace(1, 12, 12)
X, Y = np.meshgrid(xs, ys)

# Set the z axis limits, so they aren't recalculated each frame.
ax.set_zlim(-2, 0)

# Begin plotting.
wframe = None
tstart = time.time()

#output files
_0=open("0.json","w")
_1=open("1.json","w")
_2=open("2.json","w")
_3=open("3.json","w")
_4=open("4.json","w")
_5=open("5.json","w")

#interpolate to start point
for i in np.linspace(0, 1, 1000):
    Z = (np.cos(0.2 * np.pi * X)*0.5-1)*i

    wframe = ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
    plt.pause(.001)
    wframe.remove()
    
    def datafy(datatofy):
        cnt=0
        dicti={}
        listo=[]
        array=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x']
        for i in datatofy:
            for j in i:
                dicti[array[cnt]]=round(j,2)
                cnt+=1
                listo.append(round(j,2))
        dicti = json.dumps(listo)
        dicti = dicti.replace(' ','')
        dicti = dicti.replace('-','')
        dicti = dicti.replace('0.0,','0,')
        dicti+='\n'
        return dicti

    #write file data
    _0.write(datafy(Z[0:2]))
    _1.write(datafy(Z[2:4]))
    _2.write(datafy(Z[4:6]))
    _3.write(datafy(Z[6:8]))
    _4.write(datafy(Z[8:10]))
    _5.write(datafy(Z[10:]))

"""
for phi in np.linspace(0, 200/np.pi, 3000):   
    # Generate data.
    Z = np.cos(0.2 * np.pi * X + phi)*0.5-1
    # Plot the new wireframe and pause briefly before continuing.
    wframe = ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
    plt.pause(.001)
    wframe.remove()"""

for i in range(len(X)):
    print(Z[i])

print('Average FPS: %f' % (100 / (time.time() - tstart)))