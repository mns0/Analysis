import matplotlib
from matplotlib.backends.backend_pgf import FigureCanvasPgf
matplotlib.backend_bases.register_backend('pdf', FigureCanvasPgf)

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import  glob as glob
import seaborn as sns
import pandas as pd
from scipy import stats
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score





sns.set()
sns.set_style('whitegrid')
sns.set_context('poster', font_scale=2)
mpl.rcParams['axes.linewidth'] = 2.0
mpl.rcParams['axes.edgecolor'] = 'black'
colors = ['mediumturquoise']
binSize = 5 #ns

#calculate the mean velocity
#returns mean vel and std
def calcVel(time, data, binSize):
    ns_per_ele =  (time[-1] - time[0] )/ len(time)
    totalBins = int(binSize/ns_per_ele)
    #chunk the data
    posChunked  = zip( *[iter(pos)] * totalBins)
    timeChunked = zip( *[iter(time)] * totalBins)
    vels = []
    for idx, i in enumerate(posChunked):
        dx = abs(i[-1] - i[0]) * 0.1 # Ang to nm
        dt = timeChunked[idx][-1] - timeChunked[idx][0]
        vels.append(dx/dt)
    return (np.mean(vels), np.std(vels)/np.sqrt(len(posChunked)))

#returns mean vel and std
def retVels(time, data, binSize):
    ns_per_ele =  (time[-1] - time[0] )/ len(time)
    totalBins = int(binSize/ns_per_ele)
    #chunk the data
    posChunked  = zip( *[iter(pos)] * totalBins)
    timeChunked = zip( *[iter(time)] * totalBins)
    vels = []
    for idx, i in enumerate(posChunked):
        dx = abs(i[-1] - i[0]) * 0.1 # Ang to nm
        dt = timeChunked[idx][-1] - timeChunked[idx][0]
        vels.append(dx/dt)
    return vels


#applies cutoff to the data
def cleanData(time, data, direction, length):
    if direction == "y":
        if length == 10: #full
            return (time,data)
        elif length == 20:  #5ns
            idx = np.where(time < 5.0)
            idx = idx[0][-1]
            return (time[:idx],data[:idx])
        elif length == 30:  #4ns
            idx = np.where(time < 4)
            idx = idx[0][-1]
            return (time[:idx],data[:idx])
        else:                  #1.5 ns
            idx = np.where(time < 1.5)
            idx = idx[0][-1]
            return (time[:idx],data[:idx])

def plotChunks(ax_chunked, time, data, binSize):
    ns_per_ele =  (time[-1] - time[0] )/ len(time)
    totalBins = int(binSize/ns_per_ele)
    #chunk the data
    posChunked  = zip( *[iter(pos)] * totalBins)
    timeChunked = zip( *[iter(time)] * totalBins)
    for idx, i in enumerate(posChunked):
        ax_chunked.plot(timeChunked[idx],i)
    return ax_chunked

binTime = 5 #ns
directions = ["-y"]
lengths = [0, 10, 20, 30, 40]
avg_arr = []
std_arr = []
fig, ax = plt.subplots()
#fig_chunked, ax_chunked = plt.subplots()
for idx, d in enumerate(directions):
    vels_avg_dir = [0]
    vels_std_dir = [0]

    for length in lengths:
        if length == 0:
            continue
        time, y, x , z = np.loadtxt('CFSMD_POLYLENGTH_unwrapped_pos_' + str(length) + '_' + d + "_all.txt", unpack=True)
        pos = y
        if dir == 'x':
            pos = x
        vel, std = calcVel(time,pos,binTime)
        vels_avg_dir.append(vel)
        vels_std_dir.append(std)
        velLen = retVels(time, pos, binTime)
    ns_per_ele =  (time[-1] - time[0] )/ len(time)
    avg_arr.append(vels_avg_dir)
    std_arr.append(vels_std_dir)
    ax.plot(lengths,vels_avg_dir,marker='o', markersize=12, color = colors[idx])
    ax.errorbar(lengths,vels_avg_dir, yerr=vels_std_dir, color = colors[idx])
    #ax_chunked = plotChunks(ax_chunked, time, pos, binSize)


## regression
x = lengths[:-1]
y = avg_arr[0][:-1]
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
l = slope*np.array(x) + intercept











print(l)
ax.plot(x,l,color='red',lw=2)
print("rsquared",r_value**2)
ax.set_xlim((0,45))
ax.set_ylim((0,0.35))
ax.set_xticks(np.arange(0,43,10))
ax.set_title(r"Length dependence velocity")
ax.set_xlabel(r"SsDNA length [nts]")
ax.set_ylabel(r"Velocity [nm ns$^{-1}$]")
ax.text(5, 0.30, r'fit: y = %.2f + %.2f x' % (intercept, slope), fontsize=30)
ax.text(5, 0.27, r'r$^2= $ ' + format(r_value**2,'.2f'), fontsize=30)

#plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig("TEST_velocity_vs_length_-y_cfsmd.pdf")
plt.show()
