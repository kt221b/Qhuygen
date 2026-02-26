# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 12:00:52 2023

Program intended to plot Hysteresis measurements

@author: Khagesh Tanwar
"""

import qcodes
import os
import json
import h5py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.gridspec as gridspec
import matplotlib
# matplotlib.use('Qt5Agg')
from roipoly import MultiRoi, RoiPoly
# from skimage import data, color, io
from qcodes import initialise_or_create_database_at, load_by_id
from qcodes.dataset import plot_dataset
from tkinter import Tk, filedialog
# %%  
root = Tk()
root.withdraw()  # Hide the root window

db_file_path = filedialog.askopenfilename(title="Select a file")

if db_file_path:
    print("Selected file:", db_file_path)
    root.destroy()
else:
    print("No file selected")
    
qcodes.initialise_or_create_database_at(db_file_path)
        
# %%
def hex_to_RGB(hex_str):
    """ #FFFFFF -> [255,255,255]"""
    # Pass 16 to the integer function for change of base
    return [int(hex_str[i:i + 2], 16) for i in range(1, 6, 2)]

def color_gradient(c1, c2, n):
    """
    Given two hex colors, returns a color gradient
    with n colors.
    """
    assert n > 1

    c1_rgb = np.array(hex_to_RGB(c1)) / 255
    c2_rgb = np.array(hex_to_RGB(c2)) / 255
    mix_pcts = [x / (n - 1) for x in range(n)]
    rgb_colors = [((1 - mix) * c1_rgb + (mix * c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val * 255)), "02x") for val in item]) for item in rgb_colors]

def IV_plots(run_id, mode):
    """
    Plots DC, F1, F2, rmcd, kerr for an hysteresys experiment contained in the specified run.

    Parameters
    ----------
    run_id : TYPE
        ID of the hysteresys experiement in the already open database.

    Returns
    -------
    None.

    """
    
    data = qcodes.load_by_id(run_id)
    
    try:
        elm_V = data.get_parameter_data('elm_V')['elm_V']['elm_V']
    except:
        pass
    
    try:
        elm_sense = data.get_parameter_data('elm_sense')['elm_sense']['elm_sense']*1e9
    except:
        pass
    
    try:
        Ids = data.get_parameter_data('sm_Sense_Get')['sm_Sense_Get']['sm_Sense_Get']
    except:
        pass
    
    try:
        Vds = data.get_parameter_data('sm_Source_Set_Voltage')['sm_Source_Set_Voltage']['sm_Source_Set_Voltage']
    except:
        pass
    
    try:
        Vbg = data.get_parameter_data('sm1_Source_Set_Voltage')['sm1_Source_Set_Voltage']['sm1_Source_Set_Voltage']
    except:
        pass

    try:
        I_leakage = data.get_parameter_data('sm1_Sense_Get')['sm1_Sense_Get']['sm1_Sense_Get']*1e9
    except:
        pass
     

    if  mode== 'IV_K2450':
        fig, ax = plt.subplots()
        # fig , axs = plt.subplots(1,1, sharex=True, figsize=(11,7))
        c1 = "#D60000"
        c2 = "#0000FF"
        color = color_gradient(c1, c2, len(Vds))
        normalized_path = os.path.normpath(db_file_path)
        path = os.path.dirname(normalized_path)
        path = os.path.join(path, str(run_id))
        os.makedirs(path, exist_ok=True)
        
        im1 = ax.scatter(Vds, Ids, s=10, color = color)
        im1 = ax.plot(Vds, Ids, lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax.set_title('IV_K2450')
        ax.set_xlabel('Vds (Volts)', fontsize=20, family = 'Arial', color='black')  
        ax.set_ylabel('Ids (A)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
        
        # axs[1,0].axis('off')
        # axs[0,1].axis('off')
        # axs[1,1].axis('off')
    
    
        fig.tight_layout()
        fig.savefig(path + '/' + 'ID' + str(run_id) +'.png')  
        
    if  mode== 'IV_K6517B':
        fig, ax = plt.subplots()
        # fig , axs = plt.subplots(1,1, sharex=True, figsize=(11,7))
        c1 = "#D60000"
        c2 = "#0000FF"
        color = color_gradient(c1, c2, len(elm_V))
        normalized_path = os.path.normpath(db_file_path)
        path = os.path.dirname(normalized_path)
        path = os.path.join(path, str(run_id))
        os.makedirs(path, exist_ok=True)
        
        im1 = ax.scatter(elm_V, elm_sense, s=10, color = color)
        im1 = ax.plot(elm_V, elm_sense, lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax.set_title('IV_K6517B')
        ax.set_xlabel('Vds (Volts)', fontsize=20, family = 'Arial', color='black')  
        ax.set_ylabel('Ids (pA)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
        
        # axs[1,0].axis('off')
        # axs[0,1].axis('off')
        # axs[1,1].axis('off')
        
        
        fig.tight_layout()
        fig.savefig(path + '/' + 'ID' + str(run_id) +'.png')

    if  mode== 'IV_K2450_K6517B':
        fig, ax = plt.subplots()
        # fig , axs = plt.subplots(1,1, sharex=True, figsize=(11,7))
        c1 = "#D60000"
        c2 = "#0000FF"
        color = color_gradient(c1, c2, len(elm_V))
        normalized_path = os.path.normpath(db_file_path)
        path = os.path.dirname(normalized_path)
        path = os.path.join(path, str(run_id))
        os.makedirs(path, exist_ok=True)
        
        im1 = ax.scatter(elm_V, Ids, s=10, color = color)
        im1 = ax.plot(elm_V, Ids, lw=1.0, color='black')
        ax.set_title('IV_K2450_K6517B')
        ax.set_xlabel('V_ds (Volts)', fontsize=20, family = 'Arial', color='black')  
        ax.set_ylabel('I_ds (A)', fontsize=20, family = 'Arial', color='black')
        # ax.xaxis.set_major_locator(MaxNLocator(nbins=10))
        # ax.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
       
        
        fig.tight_layout()
        fig.savefig(path + '/' + 'ID' + str(run_id) +'.png')
        
        
    if  mode== 'IVg_K2450_K6517B':
        fig , axs = plt.subplots(ncols=2, sharex=True, figsize=(11,7))
        # fig , axs = plt.subplots(1,1, sharex=True, figsize=(11,7))
        c1 = "#D60000"
        c2 = "#0000FF"
        color = color_gradient(c1, c2, len(Vbg))
        normalized_path = os.path.normpath(db_file_path)
        path = os.path.dirname(normalized_path)
        path = os.path.join(path, str(run_id))
        os.makedirs(path, exist_ok=True)
        
        im1 = axs[0].scatter(Vbg, elm_sense, s=10, color = color)
        im1 = axs[0].plot(Vbg, elm_sense, lw=1.0, color='black')
        axs[0].set_title('IVg_K2450_K6517B')
        axs[0].set_xlabel('V_bg (Volts)', fontsize=20, family = 'Arial', color='black')  
        axs[0].set_ylabel('I_ds (nA)', fontsize=20, family = 'Arial', color='black')
        axs[0].xaxis.set_major_locator(MaxNLocator(nbins=10))
        # ax.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[0].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        im1 = axs[1].scatter(Vbg, I_leakage, s=10, color = 'black')
        im1 = axs[1].plot(Vbg, I_leakage, lw=1.0, color='black')
        axs[1].set_title('IV_K2450_K6517B')
        axs[1].set_xlabel('V_bg (Volts)', fontsize=20, family = 'Arial', color='black')  
        axs[1].set_ylabel('I_leakage (nA)', fontsize=20, family = 'Arial', color='black')
        axs[1].xaxis.set_major_locator(MaxNLocator(nbins=10))
        # ax.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[1].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')        
        # axs[1,0].axis('off')
        # axs[0,1].axis('off')
        # axs[1,1].axis('off')
        
        
        fig.tight_layout()
        fig.savefig(path + '/' + 'ID' + str(run_id) +'.png')