# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 12:00:52 2023

Program intended to plot Hysteresis measurements

@author: Khagesh Tanwar
"""

import qcodes
import glob
import os
import json
import h5py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib
import matplotlib.cm as cm
from matplotlib import colormaps
from scipy.ndimage import label
from scipy import signal
# matplotlib.use('Qt5Agg')
from roipoly import MultiRoi, RoiPoly
# from skimage import data, color, io
from qcodes import initialise_or_create_database_at, load_by_id
from qcodes.dataset import plot_dataset
import tkinter as tk
from tkinter import filedialog

# %%  
root = tk.Tk()
root.withdraw()  # Hide the root window

db_file_path = filedialog.askopenfilename(title="Select a file")
 
if db_file_path:
    print("Selected file:", db_file_path)
    root.destroy()
else:
    print("No file selected")
    
qcodes.initialise_or_create_database_at(db_file_path)

# %%  
if 'db_file_path' in globals() and db_file_path:
    qcodes.initialise_or_create_database_at(db_file_path)
    print("Database refreshed:", db_file_path)
else:
    print("db_file_path is not defined")
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

def hyst_plot(run_id, mode):
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
        field = data.get_parameter_data('dcli_X')['dcli_X']['cryo_mo_field']
    except:
        pass
    try:
        field = data.get_parameter_data('DCli_X')['DCli_X']['Hz_field']
    except:
        pass
    try:
        field = data.get_parameter_data('dcli_X')['dcli_X']['Hz_field']
        if field.size == 0:
            raise ValueError
    except:
        pass
    try:
        field = data.get_parameter_data('dcli_X')['dcli_X']['Hxy_field']
        if field.size == 0:
            raise ValueError
    except:
        pass

    try:
        dcX = data.get_parameter_data('dcli_X')['dcli_X']['dcli_X']*1e3
        f1X = data.get_parameter_data('f1li_X')['f1li_X']['f1li_X']*1e3
        f1Y = data.get_parameter_data('f1li_Y')['f1li_Y']['f1li_Y']*1e3
        f2X = data.get_parameter_data('f2li_X')['f2li_X']['f2li_X']*1e3
    except:
        pass    
        dcX = data.get_parameter_data('DCli_X')['DCli_X']['DCli_X']*1e3
        f1X = data.get_parameter_data('f1li_X')['f1li_X']['f1li_X']*1e3
        f1Y = data.get_parameter_data('f1li_Y')['f1li_Y']['f1li_Y']*1e3
        f2X = data.get_parameter_data('f2li_X')['f2li_X']['f2li_X']*1e3
    
    RMCD = f1X/dcX
    Kerr = f2X/dcX
    RMCD_r = np.sqrt(f1X**2+f1Y**2)
    
    
    if  mode== 'polar':
        
        fig , axs = plt.subplots(2,3, sharex=True, figsize=(11,7))
        c1 = "#3F00FF" #"#D60000"
        c2 = "#E7D5FF" #"#0000FF"
        color = color_gradient(c1, c2, len(field))
        normalized_path = os.path.normpath(db_file_path)
        path = os.path.dirname(normalized_path)
        path = os.path.join(path, str(run_id))
        if not os.path.exists(path):
            os.mkdir(path)
        
        im1 = axs[0,0].scatter(field, dcX, s=10, color = color)
        im1 = axs[0,0].plot(field, dcX, lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[0,0].set_title('Reflectivity')
        axs[0,0].set_xlabel('Hz_field (T)', fontsize=20, family = 'Arial', color='black')  
        axs[0,0].set_ylabel('DC_comp (mV)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[0,0].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        im2 = axs[0,1].scatter(field, f1X, s=10, color = color)
        im2 = axs[0,1].plot(field, f1X, lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[0,1].set_title('f1')
        axs[0,1].set_xlabel('Hz_field (T)', fontsize=20, family = 'Arial', color='black')  
        axs[0,1].set_ylabel('f1 (mV)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[0,1].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        im3 = axs[0,2].scatter(field, f2X, s=10, color = color)
        im3 = axs[0,2].plot(field, f2X, lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[0,2].set_title('f2')
        axs[0,2].set_xlabel('Hz_field (T)', fontsize=20, family = 'Arial', color='black')  
        axs[0,2].set_ylabel('f2 (mV)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[0,2].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
        
        axs[1,0].axis('off')
        
        im4 = axs[1,1].scatter(field, RMCD, s=10, color = color)
        im4 = axs[1,1].plot(field, RMCD, lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[1,1].set_title('RMCD')
        axs[1,1].set_xlabel('Hz_field (T)', fontsize=20, family = 'Arial', color='black')  
        axs[1,1].set_ylabel('RMCD (a.u.)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[1,1].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
 
        im4 = axs[1,2].scatter(field, Kerr, s=10, color = color)
        im4 = axs[1,2].plot(field, Kerr, lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[1,2].set_title('Kerr')
        axs[1,2].set_xlabel('Hz_field (T)', fontsize=20, family = 'Arial', color='black')  
        axs[1,2].set_ylabel('Kerr (a.u.)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[1,2].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
        
        fig.tight_layout()
        fig.savefig(path + '/' + 'ID' + str(run_id) +'.png')

        
    if  mode== 'y_hyst':
        fig , axs = plt.subplots(2,3, sharex=True, figsize=(11,7))
        c1 = "#3F00FF" #"#D60000"
        c2 = "#E7D5FF" #"#0000FF"
        color = color_gradient(c1, c2, len(field))
        normalized_path = os.path.normpath(db_file_path)
        path = os.path.dirname(normalized_path)
        path = os.path.join(path, str(run_id))
        if not os.path.exists(path):
            os.mkdir(path)
        
        im1 = axs[0,0].scatter(field, dcX, s=10, color = color)
        im1 = axs[0,0].plot(field, dcX, lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[0,0].set_title('Reflectivity')
        axs[0,0].set_xlabel('Hy_field (T)', fontsize=20, family = 'Arial', color='black')  
        axs[0,0].set_ylabel('DC_comp (mV)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[0,0].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
    
        im2 = axs[0,1].scatter(field, f1X, s=10, color = color)
        im2 = axs[0,1].plot(field, f1X, lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[0,1].set_title('f1')
        axs[0,1].set_xlabel('Hy_field (T)', fontsize=20, family = 'Arial', color='black')  
        axs[0,1].set_ylabel('f1 (mV)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[0,1].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
    
        im3 = axs[0,2].scatter(field, f2X, s=10, color = color)
        im3 = axs[0,2].plot(field, f2X, lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[0,2].set_title('f2')
        axs[0,2].set_xlabel('Hy_field (T)', fontsize=20, family = 'Arial', color='black')  
        axs[0,2].set_ylabel('f2 (mV)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[0,2].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
        
        axs[1,0].axis('off')
        
        im4 = axs[1,1].scatter(field, signal.savgol_filter(RMCD, 10, 1), s=10, color = color)
        im4 = axs[1,1].plot(field, signal.savgol_filter(RMCD, 10, 1), lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[1,1].set_title('RMCD')
        axs[1,1].set_xlabel('Hy_field (T)', fontsize=20, family = 'Arial', color='black')  
        axs[1,1].set_ylabel('RMCD (a.u.)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[1,1].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
     
        im6 = axs[1,2].scatter(field, signal.savgol_filter(Kerr, 10, 1), s=10, color = color)
        im6 = axs[1,2].plot(field, signal.savgol_filter(Kerr, 10, 1), lw=0.4, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[1,2].set_title('Kerr')
        axs[1,2].set_xlabel('Hy_field (T)', fontsize=20, family = 'Arial', color='black')  
        axs[1,2].set_ylabel('Kerr (a.u.)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[1,2].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
        
        fig.tight_layout()
        fig.savefig(path + '/' + 'ID' + str(run_id) +'.png')

    if  mode== 'x_hyst':
        fig , axs = plt.subplots(2,3, sharex=True, figsize=(11,7))
        c1 = "#3F00FF" #"#D60000"
        c2 = "#E7D5FF" #"#0000FF"
        color = color_gradient(c1, c2, len(field))
        normalized_path = os.path.normpath(db_file_path)
        path = os.path.dirname(normalized_path)
        path = os.path.join(path, str(run_id))
        if not os.path.exists(path):
            os.mkdir(path)
        
        im1 = axs[0,0].scatter(field, dcX, s=10, color = color)
        im1 = axs[0,0].plot(field, dcX, color='black', linewidth=0.4)
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[0,0].set_title('Reflectivity')
        axs[0,0].set_xlabel('Hx_field (T)', fontsize=20, family = 'Arial', color='black')  
        axs[0,0].set_ylabel('DC_comp (mV)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[0,0].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
    
        im2 = axs[0,1].scatter(field, f1X, s=10, color = color)
        im2 = axs[0,1].plot(field, f1X, color='black', linewidth=0.4)
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[0,1].set_title('f1')
        axs[0,1].set_xlabel('Hx_field (T)', fontsize=20, family = 'Arial', color='black')  
        axs[0,1].set_ylabel('f1 (mV)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[0,1].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
    
        im3 = axs[0,2].scatter(field, f2X, s=10, color = color)
        im3 = axs[0,2].plot(field, f2X, color='black', linewidth=0.4)
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[0,2].set_title('f2')
        axs[0,2].set_xlabel('Hx_field (T)', fontsize=20, family = 'Arial', color='black')  
        axs[0,2].set_ylabel('f2 (mV)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[0,2].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
        
        
        im4 = axs[1,0].scatter(field, Kerr, s=10, color = color)
        im4 = axs[1,0].plot(field, signal.savgol_filter(Kerr, 10, 1), color='black', linewidth=0.4)
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[1,0].set_title('Kerr_savgol')
        axs[1,0].set_xlabel('Hx_field (T)', fontsize=20, family = 'Arial', color='black')  
        axs[1,0].set_ylabel('Kerr (a.u.)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[1,0].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
        
        
        im5 = axs[1,1].scatter(field, signal.savgol_filter(RMCD, 10, 1), s=10, color = color)
        im5 = axs[1,1].plot(field, signal.savgol_filter(RMCD, 10, 1), color='black', linewidth=0.4)
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[1,1].set_title('RMCD')
        axs[1,1].set_xlabel('Hx_field (T)', fontsize=20, family = 'Arial', color='black')  
        axs[1,1].set_ylabel('RMCD (a.u.)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[1,1].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
     
        im6 = axs[1,2].scatter(field, Kerr, s=10, color = color)
        im6 = axs[1,2].plot(field, Kerr, color='black', linewidth=0.4)
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[1,2].set_title('Kerr')
        axs[1,2].set_xlabel('Hx_field (T)', fontsize=20, family = 'Arial', color='black')  
        axs[1,2].set_ylabel('Kerr (a.u.)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[1,2].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
        
        fig.tight_layout()
        fig.savefig(path + '/' + 'ID' + str(run_id) +'.png')


def field_rotation(run_id, mode):
    """
    plots kerr rmcd or DC signal with respect to field rotation.

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
        field = data.get_parameter_data('dcli_X')['dcli_X']['cryo_mo_field']
    except:
        pass
    try:
        field = data.get_parameter_data('DCli_X')['DCli_X']['Hz_field']
    except:
        pass
    try:
        field = data.get_parameter_data('dcli_X')['dcli_X']['Hz_field']
        if field.size == 0:
            raise ValueError
    except:
        pass
    try:
        field = data.get_parameter_data('dcli_X')['dcli_X']['Hxy_field']
        if field.size == 0:
            raise ValueError
    except:
        pass

    try:
        dcX = data.get_parameter_data('dcli_X')['dcli_X']['dcli_X']*1e3
        f1X = data.get_parameter_data('f1li_X')['f1li_X']['f1li_X']*1e3
        f1Y = data.get_parameter_data('f1li_Y')['f1li_Y']['f1li_Y']*1e3
        f2X = data.get_parameter_data('f2li_X')['f2li_X']['f2li_X']*1e3
    except:
        pass    
        dcX = data.get_parameter_data('DCli_X')['DCli_X']['DCli_X']*1e3
        f1X = data.get_parameter_data('f1li_X')['f1li_X']['f1li_X']*1e3
        f1Y = data.get_parameter_data('f1li_Y')['f1li_Y']['f1li_Y']*1e3
        f2X = data.get_parameter_data('f2li_X')['f2li_X']['f2li_X']*1e3
    
    RMCD = f1X/dcX
    Kerr = f2X/dcX

    if  mode== 'y_longi':
        fig , axs = plt.subplots(2,3, sharex=True, figsize=(11,7))
        c1 = "#3F00FF" #"#D60000"
        c2 = "#E7D5FF" #"#0000FF"
        color = color_gradient(c1, c2, len(field))
        normalized_path = os.path.normpath(db_file_path)
        path = os.path.dirname(normalized_path)
        path = os.path.join(path, str(run_id))
        if not os.path.exists(path):
            os.mkdir(path)
        
        im1 = axs[0,0].scatter(field, dcX, s=10, color = color)
        im1 = axs[0,0].plot(field, dcX, lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[0,0].set_title('Reflectivity')
        axs[0,0].set_xlabel('Field_vector (Theta)', fontsize=20, family = 'Arial', color='black')  
        axs[0,0].set_ylabel('DC_comp (mV)', fontsize=20, family = 'Arial', color='black')

        axs[0,0].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
    
        im2 = axs[0,1].scatter(field, f1X, s=10, color = color)
        im2 = axs[0,1].plot(field, f1X, lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[0,1].set_title('f1')
        axs[0,1].set_xlabel('Field_vector (Theta)', fontsize=20, family = 'Arial', color='black')  
        axs[0,1].set_ylabel('f1 (mV)', fontsize=20, family = 'Arial', color='black')

        axs[0,1].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
    
        im3 = axs[0,2].scatter(field, f2X, s=10, color = color)
        im3 = axs[0,2].plot(field, f2X, lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[0,2].set_title('f2')
        axs[0,2].set_xlabel('Field_vector (Theta)', fontsize=20, family = 'Arial', color='black')  
        axs[0,2].set_ylabel('f2 (mV)', fontsize=20, family = 'Arial', color='black')

        axs[0,2].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
        
        axs[1,0].axis('off')
        
        im4 = axs[1,1].scatter(field, signal.savgol_filter(RMCD, 10, 1), s=10, color = color)
        im4 = axs[1,1].plot(field, signal.savgol_filter(RMCD, 10, 1), lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[1,1].set_title('RMCD')
        axs[1,1].set_xlabel('Field_vector (Theta)', fontsize=20, family = 'Arial', color='black')  
        axs[1,1].set_ylabel('RMCD (a.u.)', fontsize=20, family = 'Arial', color='black')

        axs[1,1].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
     
        im6 = axs[1,2].scatter(field, signal.savgol_filter(Kerr, 10, 1), s=10, color = color)
        im6 = axs[1,2].plot(field, signal.savgol_filter(Kerr, 10, 1), lw=0.4, color='black')

        axs[1,2].set_title('Kerr')
        axs[1,2].set_xlabel('Field_vector (Theta)', fontsize=20, family = 'Arial', color='black')  
        axs[1,2].set_ylabel('Kerr (a.u.)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[1,2].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
        
        fig.tight_layout()
        fig.savefig(path + '/' + 'ID' + str(run_id) +'.png')

# %%        
    
root = Tk()
root.withdraw()

# Open file dialog to select a file
file_path = filedialog.askopenfilename(
    title="Select a file",
    filetypes=[("Data files", "*.txt *.dat *.csv"), ("All files", "*.*")]
)


folder = os.path.dirname(file_path)
try:
    data = np.loadtxt(file_path, usecols=(0, 2),delimiter=';', skiprows=3)
except:
    pass

try:
    data = np.loadtxt(file_path, usecols=(0, 2),delimiter='\t', skiprows=3)
except:
    pass
# %%
def hyst_plot_corrected(mode):    
    if  mode== 'polar_corr':
        fig, ax = plt.subplots(layout='constrained')
        

        field = data[:, 0]
        kerr = data[:, 1]
        kerr = signal.savgol_filter(kerr, 10, 1)
        c1 = "#3F00FF" #"#D60000"
        c2 = "#E7D5FF" #"#0000FF"
        color = color_gradient(c1, c2, len(field[472:2338]))
        
        ax.plot(field[472:2338], kerr[472:2338], label='Kerr', color='black', linewidth=0.4)
        ax.scatter(field[472:2338], kerr[472:2338], s=10, color = color)
        ax.set_ylabel('Kerr (a.u.)', fontsize=20, family = 'Arial', color='black')
        ax.set_xlabel('Hz_field (T)', fontsize=20, family = 'Arial', color='black')

        # ax.set_xticklabels(np.arange(0,225,25), fontsize=12, family = 'Times New Roman')
        # ax.set_yticklabels(np.arange(600, 1500, 100), fontsize=22, family = 'Times New Roman')
        # ax.legend([x1,y1], ["B","C"])
        ax.set_title("Kerr_corrected_cubic")
        # ax.legend(loc='best')

        ax.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig.tight_layout()        
        fig.savefig(file_path + '.png')
        

def kerr_vs_T(run_id):
    """
    Plots Kerr data with sample temperature of experiment contained in the specified run.

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
        temp = data.get_parameter_data('ls_A_temperature')['ls_A_temperature']['ls_A_temperature']
    except:
        pass
    try:
        field = data.get_parameter_data('dcli_X')['dcli_X']['cryo_mo_field']
    except:
        pass
    try:
        field = data.get_parameter_data('DCli_X')['DCli_X']['Hz_field']
    except:
        pass
    try:
        field = data.get_parameter_data('dcli_X')['dcli_X']['Hz_field']
        if field.size == 0:
            raise ValueError
    except:
        pass
    try:
        field = data.get_parameter_data('dcli_X')['dcli_X']['Hxy_field']
        if field.size == 0:
            raise ValueError
    except:
        pass

    try:
        dcX = data.get_parameter_data('dcli_X')['dcli_X']['dcli_X']*1e3
        f1X = data.get_parameter_data('f1li_X')['f1li_X']['f1li_X']*1e3
        f1Y = data.get_parameter_data('f1li_Y')['f1li_Y']['f1li_Y']*1e3
        f2X = data.get_parameter_data('f2li_X')['f2li_X']['f2li_X']*1e3
    except:
        pass    
        dcX = data.get_parameter_data('DCli_X')['DCli_X']['DCli_X']*1e3
        f1X = data.get_parameter_data('f1li_X')['f1li_X']['f1li_X']*1e3
        f1Y = data.get_parameter_data('f1li_Y')['f1li_Y']['f1li_Y']*1e3
        f2X = data.get_parameter_data('f2li_X')['f2li_X']['f2li_X']*1e3
    
    RMCD = f1X/dcX
    Kerr = f2X/dcX
        
    
    fig , axs = plt.subplots(1,3, sharex=True, figsize=(11,4))
    normalized_path = os.path.normpath(db_file_path)
    path = os.path.dirname(normalized_path)
    path = os.path.join(path, str(run_id))
    if not os.path.exists(path):
        os.mkdir(path)
    
    im1 = axs[0].scatter(temp, dcX, s=10, color = 'grey')
    im1 = axs[0].plot(temp, dcX, lw=1.0, color='black')
    # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
    axs[0].set_title('Reflectivity')
    axs[0].set_xlabel('Temperature (K)', fontsize=20, family = 'Arial', color='black')  
    axs[0].set_ylabel('DC_comp (mV)', fontsize=20, family = 'Arial', color='black')
    # ax1.set_xticklabels([])
    # ax1.set_yticklabels([])
    # ax1.set_xticks([])
    # ax1.set_yticks([])
    axs[0].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

    
    im2 = axs[1].scatter(temp, RMCD, s=10, color = 'grey')
    im2 = axs[1].plot(temp, RMCD, lw=1.0, color='black')
    # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
    axs[1].set_title('RMCD')
    axs[1].set_xlabel('Temperature (K)', fontsize=20, family = 'Arial', color='black')  
    axs[1].set_ylabel('RMCD (a.u.)', fontsize=20, family = 'Arial', color='black')
    # ax1.set_xticklabels([])
    # ax1.set_yticklabels([])
    # ax1.set_xticks([])
    # ax1.set_yticks([])
    axs[1].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
 
    im3 = axs[2].scatter(temp, Kerr, s=10, color = 'grey')
    im3 = axs[2].plot(temp, Kerr, lw=1.0, color='black')
    # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
    axs[2].set_title('Kerr')
    axs[2].set_xlabel('Temperature (K)', fontsize=20, family = 'Arial', color='black')  
    axs[2].set_ylabel('Kerr (a.u.)', fontsize=20, family = 'Arial', color='black')
    # ax1.set_xticklabels([])
    # ax1.set_yticklabels([])
    # ax1.set_xticks([])
    # ax1.set_yticks([])
    axs[2].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
    
    fig.tight_layout()
    fig.savefig(path + '/' + 'ID' + str(run_id) +'.png')