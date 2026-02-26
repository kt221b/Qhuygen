# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 12:00:52 2023

Program intended to plot MOKE measurements

@author: 34633
"""

import qcodes as qc
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt  #, gridspec
from qcodes import initialise_or_create_database_at, load_by_id
from qcodes.dataset import plot_dataset

        
# %%
# Plots
parent_dir = 'G:/My Drive/Experiments/Materials/WSe2/WSe2_LUMPY_TEkhagesh/device_0/measurements'

nIDstr = 68 + '_' 
AC_V= np.loadtxt(parent_dir + nIDstr +'/bg_V.txt', unpack=True, delimiter=';')

AC_V= np.loadtxt('G:/My Drive/Experiments/Materials/WSe2/WSe2_LUMPY_TEkhagesh/device_0/measurements/138_2_contacts_sample_IV_bg_sweep/bg_V.txt', unpack=True, delimiter=';')
bg_V= np.loadtxt('G:/My Drive/Experiments/Materials/WSe2/WSe2_LUMPY_TEkhagesh/device_0/measurements/138_2_contacts_sample_IV_bg_sweep/bg_V.txt', unpack=True, delimiter=';')
li1R= np.loadtxt('G:/My Drive/Experiments/Materials/WSe2/WSe2_LUMPY_TEkhagesh/device_0/measurements/138_2_contacts_sample_IV_bg_sweep/li1_R.txt', unpack=True, delimiter=';')
li2R= np.loadtxt('G:/My Drive/Experiments/Materials/WSe2/WSe2_LUMPY_TEkhagesh/device_0/measurements/138_2_contacts_sample_IV_bg_sweep/li2_R.txt', unpack=True, delimiter=';')
# %%
 
fig1, axs1 = plt.subplots(nrows=1, ncols=3)
axs1[0].title.set_text('Bg_vs_I')
im1 = axs1[0].scatter(bgV[:,1], li1R[:,1], s=15.0, facecolor='none', edgecolors='black')
im1 = axs1[0].plot(bgV[:,1], li1R[:,1], lw=1.0, color='black')
plt.plot(bgV[:,1],np.average(li1R[:,1]), color='red')  
axs1[0].set_xticklabels([])
axs1[0].set_yticklabels([])
axs1[0].set_xticks([])
axs1[0].set_yticks([])
axs1[0].tick_params(axis='both', length=8, which='major')
# cbar1 = fig1.colorbar(im1, ax=axs1[0], fraction=fraction)
axs1[1].title.set_text('Bg_Vds')
im2 = axs1[1].scatter(bgV[55:,1], li2R[55:,1], s=15.0, facecolor='none', edgecolors='black')
im2 = axs1[1].plot(bgV[55:,1], li2R[55:,1], lw=1.0, color='black')
axs1[1].set_xticklabels([])
axs1[1].set_yticklabels([])
axs1[1].set_xticks([])
axs1[1].set_yticks([])
# cbar2 = fig1.colorbar(im2, ax=axs1[1], fraction=fraction)
axs1[2].title.set_text('Ids_vs_Vds')
im3 = axs1[2].scatter(li1R[55:,1], li2R[55:,1], s=15.0, facecolor='none', edgecolors='black')
im3 = axs1[2].plot(li1R[55:,1], li2R[55:,1], lw=1.0, color='black')
axs1[2].set_xticklabels([])
axs1[2].set_yticklabels([])
axs1[2].set_xticks([])
axs1[2].set_yticks([])
# cbar3 = fig1.colorbar(im3, ax=axs1[2], fraction=fraction)
fig1.tight_layout()
fig1.show()
fig1.savefig('G:/My Drive/Experiments/Materials/WSe2/WSe2_LUMPY_TEkhagesh/device_0/measurements/138_2_contacts_sample_IV_bg_sweep/149.tif')
