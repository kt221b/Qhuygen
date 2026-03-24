# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 12:00:52 2023

Program intended to plot MOKE measurements

@author: 34633
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = [8, 5]
fig, ax = plt.subplots()
ax.set_ylim(-1, 0.4)
ax.set_xlim(0, 1.4)
#ax.set_xlim(-1, 1)

#total density of states (plot1 & plot1a)
x1, y1, y2 = np.loadtxt('BAND1.dat', usecols=(0,1,2), unpack = True)

# %%
# Print all the experiment info


# %%
# Select dataset
nID = 85
dset = qc.dataset.load_by_id(nID)

# %%
data = dset.to_xarray_dataarray_dict()
name = dset.name

# %%
# Plots
# Common parameters
aspect = 1.9
fraction = 0.025

fig1, axs1 = plt.subplots(nrows=1, ncols=3)
axs1[0].title.set_text('Reflection')
im1 = axs1[0].imshow(DCx, aspect=aspect, cmap='Greys') # aspect='auto', 'equal'
axs1[0].set_xticklabels([])
axs1[0].set_yticklabels([])
axs1[0].set_xticks([])
axs1[0].set_yticks([])
cbar1 = fig1.colorbar(im1, ax=axs1[0], fraction=fraction)
axs1[1].title.set_text('Kerr rotation')
im2 = axs1[1].imshow(Kerrcor, aspect=aspect, cmap='bwr', vmin=-maxabsKerr, vmax=maxabsKerr)
axs1[1].set_xticklabels([])
axs1[1].set_yticklabels([])
axs1[1].set_xticks([])
axs1[1].set_yticks([])
cbar2 = fig1.colorbar(im2, ax=axs1[1], fraction=fraction)
axs1[2].title.set_text('RMCD')
im3 = axs1[2].imshow(RMCDcor, aspect=aspect, cmap='bwr', vmin=-maxabsRMCD, vmax=maxabsRMCD)
axs1[2].set_xticklabels([])
axs1[2].set_yticklabels([])
axs1[2].set_xticks([])
axs1[2].set_yticks([])
cbar3 = fig1.colorbar(im3, ax=axs1[2], fraction=fraction)
fig1.tight_layout()
fig1.show()
fig1.savefig('85.pdf')


