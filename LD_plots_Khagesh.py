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
import matplotlib.gridspec as gridspec
import matplotlib
# matplotlib.use('Qt5Agg')
# from roipoly import MultiRoi, RoiPoly
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
# def hex_to_RGB(hex_str):
#     """ #FFFFFF -> [255,255,255]"""
#     # Pass 16 to the integer function for change of base
#     return [int(hex_str[i:i + 2], 16) for i in range(1, 6, 2)]

# def color_gradient(c1, c2, n):
#     """
#     Given two hex colors, returns a color gradient
#     with n colors.
#     """
#     assert n > 1

#     c1_rgb = np.array(hex_to_RGB(c1)) / 255
#     c2_rgb = np.array(hex_to_RGB(c2)) / 255
#     mix_pcts = [x / (n - 1) for x in range(n)]
#     rgb_colors = [((1 - mix) * c1_rgb + (mix * c2_rgb)) for mix in mix_pcts]
#     return ["#" + "".join([format(int(round(val * 255)), "02x") for val in item]) for item in rgb_colors]
def LD_plot(run_id, mode):
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
        angle = data.get_parameter_data('dcli_X')['dcli_X']['LDmotor_angle']
    except:
        pass
    

    #     field = data.get_parameter_data('dcli_X')['dcli_X']['Hz_field']
    #     if field.size == 0:
    #         raise ValueError
    # except:
    #     pass
    # try:
    #     field = data.get_parameter_data('dcli_X')['dcli_X']['Hxy_field']
    #     if field.size == 0:
    #         raise ValueError
    # except:
    #     pass
    
    dcX = data.get_parameter_data('dcli_X')['dcli_X']['dcli_X']*1e3
    f2X = data.get_parameter_data('f2li_X')['f2li_X']['f2li_X']*1e3

    LD = f2X/dcX

    
    if  mode== 'LD':
        
        fig , axs = plt.subplots(2,2, sharex=True, figsize=(11,7), subplot_kw={'projection': 'polar'})
        # c1 = "#D60000"
        # c2 = "#0000FF"
        # color = color_gradient(c1, c2, len(angle))
        normalized_path = os.path.normpath(db_file_path)
        path = os.path.dirname(normalized_path)
        path = os.path.join(path, str(run_id))

        # os.mkdir(path)
        
        im1 = axs[0,0].scatter(np.radians(angle)*2, (dcX), s=10, color = 'black')
        im1 = axs[0,0].plot(np.radians(angle)*2, (dcX), lw=1.0, color='black')
        
        # axs[0,0].set_xticks(np.radians([0, 30, 60, 90, 120, 150, 180]))
        axs[0,0].set_rticks(np.arange(0, 500, 100))  # Less radial ticks
        axs[0,0].set_rlabel_position(-22.5)  # Move radial labels away from plotted line
        axs[0,0].grid(True)
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        # axs[0,0].set_title('Reflectivity')
        # axs[0,0].set_xlabel('Hz_field (T)', fontsize=20, family = 'Arial', color='black')  
        # axs[0,0].set_ylabel('DC_comp (mV)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        # axs[0,0].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')


        im2 = axs[0,1].scatter(np.radians(angle)*2, (f2X), s=10, color = 'red')
        im2 = axs[0,1].plot(np.radians(angle)*2, (f2X), lw=1.0, color='red')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        # axs[0,2].set_title('f2')
        # axs[0,2].set_xlabel('angle (Theta)', fontsize=20, family = 'Arial', color='black')  
        # axs[0,2].set_ylabel('f2 (mV)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        # axs[0,2].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
        
        axs[1,0].axis('off')
        
 
        im3 = axs[1,1].scatter(np.radians(angle)*2, (LD), s=10, color = 'blue')
        im3 = axs[1,1].plot(np.radians(angle)*2, (LD), lw=1.0, color='blue')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        # axs[1,2].set_title('Kerr')
        # axs[1,2].set_xlabel('Hz_field (T)', fontsize=20, family = 'Arial', color='black')  
        # axs[1,2].set_ylabel('Kerr (a.u.)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        # axs[1,2].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
        
        fig.tight_layout()
        # fig.savefig(path + '/' + 'ID' + str(run_id) +'.png')
        
def LD_plot_sio2(run_id1, run_id2, mode):
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
    
    data = qcodes.load_by_id(run_id1)
    data_sio2 = qcodes.load_by_id(run_id2)
    
    try:
        angle = data.get_parameter_data('dcli_X')['dcli_X']['LDmotor_angle']
    except:
        pass
    
    try:
        angle_sio2 = data_sio2.get_parameter_data('dcli_X')['dcli_X']['LDmotor_angle']
    except:
        pass
    # try:
    #     field = data.get_parameter_data('dcli_X')['dcli_X']['Hz_field']
    #     if field.size == 0:
    #         raise ValueError
    # except:
    #     pass
    # try:
    #     field = data.get_parameter_data('dcli_X')['dcli_X']['Hxy_field']
    #     if field.size == 0:
    #         raise ValueError
    # except:
    #     pass
    
    dcX = data.get_parameter_data('dcli_X')['dcli_X']['dcli_X']*1e3
    f2X = data.get_parameter_data('f2li_X')['f2li_X']['f2li_X']*1e3
    dcX_sio2 = data_sio2.get_parameter_data('dcli_X')['dcli_X']['dcli_X']*1e3
    f2X_sio2 = data_sio2.get_parameter_data('f2li_X')['f2li_X']['f2li_X']*1e3
    LD = f2X/dcX
    LD_sio2 = f2X_sio2/dcX_sio2

    if  mode== 'LD':
        
        fig , axs = plt.subplots(2,2, sharex=True, figsize=(11,7), subplot_kw={'projection': 'polar'})
        # c1 = "#D60000"
        # c2 = "#0000FF"
        # color = color_gradient(c1, c2, len(angle))
        normalized_path = os.path.normpath(db_file_path)
        path = os.path.dirname(normalized_path)

        # os.mkdir(path)
        
        im1 = axs[0,0].scatter(np.radians(angle)*2, abs(dcX), s=20, color = 'black')
        im1 = axs[0,0].scatter(np.radians(angle_sio2)*2, abs(dcX_sio2), s=10, color = 'red')
        
        im1 = axs[0,0].plot(np.radians(angle)*2, abs(dcX), lw=1.0, color='black')
        im1 = axs[0,0].plot(np.radians(angle_sio2)*2, abs(dcX_sio2), lw=1.0, color='red')
        # axs[0,0].set_xticks(np.radians([0, 30, 60, 90, 120, 150, 180]))
        axs[0,0].set_rticks(np.linspace(0, max(dcX)+max(dcX)/10, 5))  # Less radial ticks
        axs[0,0].set_rlabel_position(22.5)  # Move radial labels away from plotted line
        axs[0,0].grid(True)
        axs[0,0].set_title('Reflectivity')
        # axs[0,0].set_xlabel('Hz_field (T)', fontsize=20, family = 'Arial', color='black')  
        # axs[0,0].set_ylabel('DC_comp (mV)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        # axs[0,0].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        im2 = axs[0,1].scatter(np.radians(angle)*2, abs(f2X), s=20, color = 'black')
        im2 = axs[0,1].scatter(np.radians(angle_sio2)*2, abs(f2X_sio2), s=10, color = 'red')
        
        im1 = axs[0,1].plot(np.radians(angle)*2, abs(f2X), lw=1.0, color='black')
        im1 = axs[0,1].plot(np.radians(angle_sio2)*2, abs(f2X_sio2), lw=1.0, color='red')
        
        # axs[0,0].set_xticks(np.radians([0, 30, 60, 90, 120, 150, 180]))
        axs[0,1].set_rticks(np.linspace(0, max(f2X), 5))  # Less radial ticks
        axs[0,1].set_rlabel_position(22.5)  # Move radial labels away from plotted line
        axs[0,1].grid(True)
        axs[0,1].set_title('f2')
        # axs[0,2].set_xlabel('angle (Theta)', fontsize=20, family = 'Arial', color='black')  
        # axs[0,2].set_ylabel('f2 (mV)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        # axs[0,2].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
        
        axs[1,0].axis('off')
        
 
        im1 = axs[1,1].scatter(np.radians(angle)*2, abs(LD), s=20, color = 'black')
        im1 = axs[1,1].scatter(np.radians(angle_sio2)*2, abs(LD_sio2), s=10, color = 'red')
        
        im1 = axs[1,1].plot(np.radians(angle)*2, abs(LD), lw=1.0, color='black')
        im1 = axs[1,1].plot(np.radians(angle_sio2)*2, abs(LD_sio2), lw=1.0, color='red')
        
        # axs[0,0].set_xticks(np.radians([0, 30, 60, 90, 120, 150, 180]))
        axs[1,1].set_rticks(np.linspace(0, max(LD), 5))  # Less radial ticks
        axs[1,1].set_rlabel_position(22.5)  # Move radial labels away from plotted line
        axs[1,1].grid(True)
        axs[1,1].set_title('LD')
        # axs[1,2].set_xlabel('Hz_field (T)', fontsize=20, family = 'Arial', color='black')  
        # axs[1,2].set_ylabel('Kerr (a.u.)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        # axs[1,2].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
        
        fig.tight_layout()
        fig.savefig(path + '/' + 'LD' + str(run_id1) + '_'+ str(run_id2) +'.png')
        
