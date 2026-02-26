# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 12:00:52 2023

Program intended to plot Hysteresis measurements

@author: Khagesh Tanwar
"""

import qcodes as qc
import os
import json
import h5py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
    
qc.initialise_or_create_database_at(db_file_path)


# %%  
# print(experiments) Polar Hysteresis

field = data.get_parameter_data('dcli_X')['dcli_X']['Hz_field']
# Hz_field = data['Hz_field'].data



dcX = data.get_parameter_data('dcli_X')['dcli_X']['dcli_X']*1e3
f1X = data.get_parameter_data('f1li_X')['f1li_X']['f1li_X']*1e3
f2X = data.get_parameter_data('f2li_X')['f2li_X']['f2li_X']*1e3

Kerr = (f2X/dcX)
RMCD = (f1X/dcX)  


# %%
# Export data


def Export_data_csv(run_id, mode):
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
    
    data = qc.load_by_id(run_id)
    
    # try:
    #     field = data.get_parameter_data('dcli_X')['dcli_X']['cryo_mo_field']
    # except:
    #     pass
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
    
    try:
        dcX = data.get_parameter_data('dcli_dcli_buffer_X')['dcli_dcli_buffer_X']['dcli_dcli_buffer_X']
        f1X = data.get_parameter_data('f1li_f1li_buffer_X')['f1li_f1li_buffer_X']['f1li_f1li_buffer_X']
        f2X = data.get_parameter_data('f2li_f2li_buffer_X')['f2li_f2li_buffer_X']['f2li_f2li_buffer_X']
    except:
        pass
    try:
        dcX = data.get_parameter_data('dcli_ch1_databuffer')['dcli_ch1_databuffer']['dcli_ch1_databuffer']
        f1X = data.get_parameter_data('f1li_ch1_databuffer')['f1li_ch1_databuffer']['f1li_ch1_databuffer']
        f2X = data.get_parameter_data('f2li_ch1_databuffer')['f2li_ch1_databuffer']['f2li_ch1_databuffer']
    except:
        pass
    try:
        dcX = data.get_parameter_data('dcli_X')['dcli_X']['dcli_X']
        f1X = data.get_parameter_data('f1li_X')['f1li_X']['f1li_X']
        f2X = data.get_parameter_data('f2li_X')['f2li_X']['f2li_X']
        dcX=dcX.reshape(100, 100)
        f1X=f1X.reshape(100, 100)
        f2X=f2X.reshape(100, 100)
    except:
        pass
    
    RMCD = f1X/dcX
    Kerr = f2X/dcX

    normalized_path = os.path.normpath(db_file_path)
    path = os.path.dirname(normalized_path)
    path = os.path.join(path, str(run_id))
    if not os.path.exists(path):
        os.mkdir(path)
        
    if mode == 'polar':

        df2 = pd.DataFrame(RMCD)
        file_name2 = path + '/RMCD.csv'
        df2.to_csv(file_name2, sep=';', encoding='utf-8', index = False)
        
        df3 = pd.DataFrame(Kerr)
        file_name3 = path + '/Kerr.csv'
        df3.to_csv(file_name3, sep=';', encoding='utf-8', index = False)
        
        df4 = pd.DataFrame(f1X)
        file_name4 = path + '/f1.csv'
        df4.to_csv(file_name4, sep=';', encoding='utf-8', index = False)
        
        df5 = pd.DataFrame(f2X)
        file_name5 = path + '/f2.csv'
        df5.to_csv(file_name5, sep=';', encoding='utf-8', index = False)
        
        df6 = pd.DataFrame(dcX)
        file_name6 = path + '/DC.csv'
        df6.to_csv(file_name6, sep=';', encoding='utf-8', index = False)
        
# %%
# Plots
# parent_dir = "G:\\My Drive\\Experiments\\Materials\\CrTe2\\CVT_acitonitrile_iodine_3rd_try\\MOKE\\sample6\\"
# parent_dir_ivo1 = "G:\\My Drive\\Experiments\\Materials\\CrCl3\\crcl3_KH\\sample1\\"
parent_dir_ivo = "G:\\My Drive\\Experiments\\Materials\\CrSBr\\20250310_reyes_sample_kh\\exfo1\\"
# parent_dir_maintenance = "C:\\Users\\cryogenic\\Desktop\\qcodes_measurements\\Maintenance\\"

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

def plot_graph_polar(mode = 'DC'):
    if mode == 'DC':
        path = parent_dir_ivo + str(nID) + '_' + name
        Hz_field= np.loadtxt(path +'/Hz_field.csv'.format(nID), unpack=True, delimiter=';')
        Hz_field = Hz_field[::5]
        DC= np.loadtxt(path +'/DC.csv'.format(nID), unpack=True, delimiter=';')
        DC = DC[::5]
        title = 'DC_Hyst{}'.format(nID)
        fig1, ax1 = plt.subplots()
        ax1.title.set_text(title)
        c1 = "#D60000"
        c2 = "#0000FF"

        color = color_gradient(c1, c2, len(Hz_field[:,1]))
        
        im1 = ax1.scatter(Hz_field[:,1], DC[:,1], s=100, color = color)
        im1 = ax1.plot(Hz_field[:,1], DC[:,1], lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Hz_field (T)', fontsize=30, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('DC_comp (V)', fontsize=30, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.png')
        
    if mode == 'RMCD':
        path = parent_dir_ivo + str(nID) + '_' + name
        Hz_field= np.loadtxt(path +'/Hz_field.csv'.format(nID), unpack=True, delimiter=';')
        Hz_field = Hz_field[::5]
        RMCD= np.loadtxt(path +'/RMCD.csv'.format(nID), unpack=True, delimiter=';')
        RMCD = RMCD[::5]
        
        title = 'RMCD_Hyst1{}'.format(nID)
        fig1, ax1 = plt.subplots()
        ax1.title.set_text(title)
        c1 = "#D60000"
        c2 = "#0000FF"      
        color = color_gradient(c1, c2, len(Hz_field[:,1]))
        im1 = ax1.scatter(Hz_field[:,1],RMCD[:,1], s=100.0, color=color, edgecolors = 'none')
        im1 = ax1.plot(Hz_field[:,1], RMCD[:,1], lw=1.0, color='black')
        
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Hz_field (T)', fontsize=30, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('RMCD (a.u.)', fontsize=30, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.png')
        
    elif mode == 'Kerr':
        path = parent_dir_ivo + str(nID) + '_' + name
        Hz_field= np.loadtxt(path +'/Hz_field.csv'.format(nID), unpack=True, delimiter=';')
        Hz_field = Hz_field[::5]
        Kerr= np.loadtxt(path +'/Kerr.csv'.format(nID), unpack=True, delimiter=';')
        Kerr = Kerr[::5]
        title = 'Kerr_Hyst{}'.format(nID)
        fig1, ax1 = plt.subplots()
        ax1.title.set_text(title)
        c1 = "#D60000"
        c2 = "#0000FF"       
        color = color_gradient(c1, c2, len(Hz_field[:,1]))
        im1 = ax1.scatter(Hz_field[:,1],Kerr[:,1], s=100.0, color=color)
        im1 = ax1.plot(Hz_field[:,1], Kerr[:,1], lw=1.0, color='black')        
        
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Hz_field (T)', fontsize=30, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Kerr (a.u.)', fontsize=30, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.png')
        
def plot_graph_polar_sio2_removed(mode = 'DC'):
    
    path = "G:\\My Drive\\Experiments\\Materials\\CrSBr\\20250310_reyes_sample_kh\\5_4.7K_1T"
    path_sio2 = "G:\\My Drive\\Experiments\\Materials\\CrSBr\\20250310_reyes_sample_kh\\8_4.7K_1T"
    
    Hz_field= np.loadtxt(path + '/Hz_field.csv', unpack=True, delimiter=';')
    Hz_field = Hz_field[::1]
    DC= np.loadtxt(path +'/DC.csv', unpack=True, delimiter=';')
    DC = DC[::1]
    
    Hz_field_sio2= np.loadtxt(path_sio2 + '/Hz_field.csv', unpack=True, delimiter=';')
    Hz_field_sio2 = Hz_field[::1]
    DC_sio2= np.loadtxt(path_sio2 +'/DC.csv', unpack=True, delimiter=';')
    DC_sio2 = DC_sio2[::1]
        
    DC_bg = DC/DC_sio2
    
    if mode == 'DC':
  
        title = 'DC_Hyst_bg_removed_nID27'
        fig1, ax1 = plt.subplots()
        ax1.title.set_text(title)
        c1 = "#D60000"
        c2 = "#0000FF"

        color = color_gradient(c1, c2, len(Hz_field[:,1]))
        
        im1 = ax1.scatter(Hz_field[:,1], DC_bg[:,1], s=100, facecolor = color, edgecolors = 'none')
        im1 = ax1.plot(Hz_field[:,1], DC_bg[:,1], lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Hz_field (T)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('DC_comp (V)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.png')
        
    if mode == 'RMCD':
        Hz_field= np.loadtxt(path + '/Hz_field.csv', unpack=True, delimiter=';')
        Hz_field = Hz_field[::1]
        f1x= np.loadtxt(path +'/f1x.csv', unpack=True, delimiter=';')
        f1x = f1x[::1]
        
        Hz_field_sio2= np.loadtxt(path_sio2 + '/Hz_field.csv', unpack=True, delimiter=';')
        Hz_field_sio2 = Hz_field[::1]
        f1x_sio2= np.loadtxt(path_sio2 +'/f1x.csv', unpack=True, delimiter=';')
        f1x_sio2 = f1x_sio2[::1]
        
        RMCD_bg = (f1x/f1x_sio2)/((DC/DC_sio2))
        
        title = 'RMCD_Hyst_bg_removed_nID27'
        fig1, ax1 = plt.subplots()
        ax1.title.set_text(title)
        c1 = "#D60000"
        c2 = "#0000FF"      
        color = color_gradient(c1, c2, len(Hz_field[:,1]))
        im1 = ax1.scatter(Hz_field[:,1],RMCD_bg[:,1], s=40.0, color=color)
        im1 = ax1.plot(Hz_field[326:,1], RMCD_bg[326:,1], lw=1.0, color='black')
        
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Hz_field (T)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('RMCD (V)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.png')
        
    elif mode == 'Kerr':
        Hz_field= np.loadtxt(path + '/Hz_field.csv', unpack=True, delimiter=';')
        Hz_field = Hz_field[::1]
        f2x= np.loadtxt(path +'/f2x.csv', unpack=True, delimiter=';')
        f2x = f2x[::1]
        
        Hz_field_sio2= np.loadtxt(path_sio2 + '/Hz_field.csv', unpack=True, delimiter=';')
        Hz_field_sio2 = Hz_field_sio2[::1]
        f2x_sio2= np.loadtxt(path_sio2 +'/f2x.csv', unpack=True, delimiter=';')
        f2x_sio2 = f2x_sio2[::1]
        
        Kerr_bg = (f2x/DC)/((f2x_sio2/DC_sio2))
        

        title = 'Kerr_Hyst{}_bg_removed_nID27'
        fig1, ax1 = plt.subplots()
        ax1.title.set_text(title)
        c1 = "#D60000"
        c2 = "#0000FF"       
        color = color_gradient(c1, c2, len(Hz_field[:,1]))
        im1 = ax1.scatter(Hz_field[:,1],Kerr_bg[:,1], s=40.0, color=color)
        im1 = ax1.plot(Hz_field[326:,1], Kerr_bg[326:,1], lw=1.0, color='black')        
        
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Hz_field (T)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Kerr (V)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.png')        
        
def plot_graph_inplane(mode = 'DC'):
    if mode == 'DC':
        path = parent_dir_ivo + str(nID) + '_' + name
        Hxy_field= np.loadtxt(path +'/Hxy_field.csv'.format(nID), unpack=True, delimiter=';')
        Hxy_field = Hxy_field[::20]
        DC= np.loadtxt(path +'/DC.csv'.format(nID), unpack=True, delimiter=';')
        DC = DC[::20]
        title = 'DC_Hyst{}'.format(nID)
        fig1, ax1 = plt.subplots()
        ax1.title.set_text(title)
        c1 = "#D60000"
        c2 = "#0000FF"

        color = color_gradient(c1, c2, len(Hxy_field[:,1]))
        
        im1 = ax1.scatter(Hxy_field[:,1], DC[:,1], s=30, facecolor = color, edgecolors = 'none')
        im1 = ax1.plot(Hxy_field[:,1], DC[:,1], lw=0.50, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Hxy_field (T)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('DC_comp (V)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.png')
        
    if mode == 'RMCD':
        path = parent_dir_ivo + str(nID) + '_' + name
        Hxy_field= np.loadtxt(path +'/Hxy_field.csv'.format(nID), unpack=True, delimiter=';')
        Hxy_field = Hxy_field[::20]
        RMCD= np.loadtxt(path +'/RMCD.csv'.format(nID), unpack=True, delimiter=';')
        RMCD = RMCD[::20]
        
        title = 'RMCD_Hyst{}'.format(nID)
        fig1, ax1 = plt.subplots()
        ax1.title.set_text(title)
        c1 = "#D60000"
        c2 = "#0000FF"      
        color = color_gradient(c1, c2, len(Hxy_field[:,1]))
        im1 = ax1.scatter(Hxy_field[:,1],RMCD[:,1], s=10.0, color=color)
        im1 = ax1.plot(Hxy_field[:,1], RMCD[:,1], lw=0.50, color='black')
        
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Hxy_field (T)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('RMCD (a.u.)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.png')
        
    elif mode == 'Kerr':
        path = parent_dir_ivo + str(nID) + '_' + name
        Hxy_field= np.loadtxt(path +'/Hxy_field.csv'.format(nID), unpack=True, delimiter=';')
        Hxy_field = Hxy_field[::20]
        Kerr= np.loadtxt(path +'/Kerr.csv'.format(nID), unpack=True, delimiter=';')
        Kerr = Kerr[::20]
        title = 'Kerr_Hyst{}'.format(nID)
        fig1, ax1 = plt.subplots()
        ax1.title.set_text(title)
        c1 = "#D60000"
        c2 = "#0000FF"       
        color = color_gradient(c1, c2, len(Hxy_field[:,1]))
        im1 = ax1.scatter(Hxy_field[:,1],Kerr[:,1], s=10.0, color=color)
        im1 = ax1.plot(Hxy_field[:,1], Kerr[:,1], lw=0.50, color='black')        
        
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Hxy_field (T)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Kerr (a.u.)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.png')        
        
def plot_graph_inplane_sio2_removed(mode = 'DC'):
    
    path = "G:\\My Drive\\Experiments\\Materials\\NiBr2\\20240321_CVD_flakes_MOKE_cryovac\\sample5\\37_x_BFP_hysteresis_NiBr2_31.3K_at_10x_14.6y_of_id16"
    path_sio2 = "G:\\My Drive\\Experiments\\Materials\\NiBr2\\20240321_CVD_flakes_MOKE_cryovac\\sample5\\38_x_BFP_hysteresis_sio2_31.3K_at_10x_14.6y_of_id16"
    
    Hxy_field= np.loadtxt(path + '/Hxy_field.csv', unpack=True, delimiter=';')
    Hxy_field1 = Hxy_field[::50]
    DC= np.loadtxt(path +'/DC.csv', unpack=True, delimiter=';')
    DC = DC[::50]
    
    Hxy_field_sio2= np.loadtxt(path_sio2 + '/Hxy_field.csv', unpack=True, delimiter=';')
    Hxy_field1_sio2 = Hxy_field[::50]
    DC_sio2= np.loadtxt(path_sio2 +'/DC.csv', unpack=True, delimiter=';')
    DC_sio2 = DC_sio2[::50]
    
    DC_bg = DC-DC_sio2
    
    if mode == 'DC':

        
        title = 'DC_Hyst_bg_removed_nID27'
        fig1, ax1 = plt.subplots()
        ax1.title.set_text(title)
        c1 = "#D60000"
        c2 = "#0000FF"

        color = color_gradient(c1, c2, len(Hxy_field1[:,1]))
        
        im1 = ax1.scatter(Hxy_field1[:,1], DC_bg[:,1], s=100, facecolor = color, edgecolors = 'none')
        im1 = ax1.plot(Hxy_field1[:,1], DC_bg[:,1], lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Hxy_field (T)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('DC_comp (V)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.png')
        
    if mode == 'RMCD':
        Hxy_field= np.loadtxt(path + '/Hxy_field.csv', unpack=True, delimiter=';')
        Hxy_field1 = Hxy_field[::50]
        f1x= np.loadtxt(path +'/f1x.csv', unpack=True, delimiter=';')
        f1x = f1x[::50]
        
        Hxy_field_sio2= np.loadtxt(path_sio2 + '/Hxy_field.csv', unpack=True, delimiter=';')
        Hxy_field1_sio2 = Hxy_field[::50]
        f1x_sio2= np.loadtxt(path_sio2 +'/f1x.csv', unpack=True, delimiter=';')
        f1x_sio2 = f1x_sio2[::50]
        
        RMCD_bg = (f1x-f1x_sio2)/DC
        
        title = 'RMCD_Hyst_bg_removed_nID27'
        fig1, ax1 = plt.subplots()
        ax1.title.set_text(title)
        c1 = "#D60000"
        c2 = "#0000FF"      
        color = color_gradient(c1, c2, len(Hxy_field1[:,1]))
        im1 = ax1.scatter(Hxy_field1[:,1],RMCD_bg[:,1], s=100.0, color=color)
        im1 = ax1.plot(Hxy_field1[:,1], RMCD_bg[:,1], lw=1.0, color='black')
        
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Hxy_field (T)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('RMCD (a.u.)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.png')
        
    elif mode == 'Kerr':
        Hxy_field= np.loadtxt(path + '/Hxy_field.csv', unpack=True, delimiter=';')
        Hxy_field = Hxy_field[::50]
        f2x= np.loadtxt(path +'/f2x.csv', unpack=True, delimiter=';')
        f2x = f2x[::50]
        
        Hxy_field_sio2= np.loadtxt(path_sio2 + '/Hxy_field.csv', unpack=True, delimiter=';')
        Hxy_field_sio2 = Hxy_field_sio2[::50]
        f2x_sio2= np.loadtxt(path_sio2 +'/f2x.csv', unpack=True, delimiter=';')
        f2x_sio2 = f2x_sio2[::50]
        
        Kerr_bg = (f2x-f2x_sio2)/DC
        

        title = 'Kerr_Hyst{}_bg_removed_nID27'
        fig1, ax1 = plt.subplots()
        ax1.title.set_text(title)
        c1 = "#D60000"
        c2 = "#0000FF"       
        color = color_gradient(c1, c2, len(Hxy_field1[:,1]))
        im1 = ax1.scatter(Hxy_field[:,1],Kerr_bg[:,1], s=100.0, color=color)
        im1 = ax1.plot(Hxy_field[:,1], Kerr_bg[:,1], lw=1.0, color='black')        
        
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Hxy_field (T)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Kerr (a.u.)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.png')        
        
def plot_graph_maintenance():
        
        parent_dir_maintenance = "C:\\Users\\cryogenic\\Desktop\\qcodes_measurements\\Maintenance\\"
        path = parent_dir_maintenance + str(nID) + '_' + name

        time= np.loadtxt(path +'/time.csv'.format(nID), unpack=True, delimiter=';')
        
        Hz_field= np.loadtxt(path +'/Hz_field.csv'.format(nID), unpack=True, delimiter=';')

        Hz_current= np.loadtxt(path +'/Hz_current.csv'.format(nID), unpack=True, delimiter=';')
        
        Hz_voltage= np.loadtxt(path +'/Hz_voltage.csv'.format(nID), unpack=True, delimiter=';')
        
        title = 'time vs Hz_field{}'.format(nID)
        fig1, ax1 = plt.subplots()
        ax1.title.set_text(title)



        
        im1 = ax1.scatter(time[:,1], Hz_field[:,1], s=100, edgecolors = 'none')
        im1 = ax1.plot(time[:,1], Hz_field[:,1], lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('time (Sec)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Hz_field (T)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.tif')


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
    
    dcX = data.get_parameter_data('dcli_X')['dcli_X']['dcli_X']*1e3
    f1X = data.get_parameter_data('f1li_X')['f1li_X']['f1li_X']*1e3
    f2X = data.get_parameter_data('f2li_X')['f2li_X']['f2li_X']*1e3
    

    
    if  mode== 'polar':
        fig , axs = plt.subplots(2,3, sharex=True, figsize=(11,7))
        c1 = "#D60000"
        c2 = "#0000FF"
        color = color_gradient(c1, c2, len(field))
        normalized_path = os.path.normpath(db_file_path)
        path = os.path.dirname(normalized_path)
        path = os.path.join(path, str(run_id))
        os.mkdir(path)
        
        im1 = axs[0,0].scatter(field, dcX, s=10, color = color)
        im1 = axs[0,0].plot(field, dcX, lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[0,0].set_title('Reflectivity')
        axs[0,0].set_xlabel('Hz_field (T)', fontsize=20, family = 'Arial', color='black')  
        axs[0,0].set_ylabel('DC_comp (V)', fontsize=20, family = 'Arial', color='black')
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
        axs[0,1].set_ylabel('f1 (V)', fontsize=20, family = 'Arial', color='black')
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
        axs[0,2].set_ylabel('f2 (V)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[0,2].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
        
        axs[1,0].axis('off')
        
        im4 = axs[1,1].scatter(field, f2X, s=10, color = color)
        im4 = axs[1,1].plot(field, f2X, lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[1,1].set_title('RMCD')
        axs[1,1].set_xlabel('Hz_field (T)', fontsize=20, family = 'Arial', color='black')  
        axs[1,1].set_ylabel('RMCD (a.u.)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[1,1].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
 
        im4 = axs[1,2].scatter(field, f2X, s=10, color = color)
        im4 = axs[1,2].plot(field, f2X, lw=1.0, color='black')
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
        c1 = "#D60000"
        c2 = "#0000FF"
        color = color_gradient(c1, c2, len(field))
        normalized_path = os.path.normpath(db_file_path)
        path = os.path.dirname(normalized_path)
        path = os.path.join(path, str(run_id))
        os.mkdir(path)
        
        im1 = axs[0,0].scatter(field, dcX, s=10, color = color)
        im1 = axs[0,0].plot(field, dcX, lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[0,0].set_title('Reflectivity')
        axs[0,0].set_xlabel('Hy_field (T)', fontsize=20, family = 'Arial', color='black')  
        axs[0,0].set_ylabel('DC_comp (V)', fontsize=20, family = 'Arial', color='black')
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
        axs[0,1].set_ylabel('f1 (V)', fontsize=20, family = 'Arial', color='black')
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
        axs[0,2].set_ylabel('f2 (V)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[0,2].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
        
        axs[1,0].axis('off')
        
        im4 = axs[1,1].scatter(field, f2X, s=10, color = color)
        im4 = axs[1,1].plot(field, f2X, lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        axs[1,1].set_title('RMCD')
        axs[1,1].set_xlabel('Hy_field (T)', fontsize=20, family = 'Arial', color='black')  
        axs[1,1].set_ylabel('RMCD (a.u.)', fontsize=20, family = 'Arial', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        axs[1,1].tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
     
        im4 = axs[1,2].scatter(field, f2X, s=10, color = color)
        im4 = axs[1,2].plot(field, f2X, lw=1.0, color='black')
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