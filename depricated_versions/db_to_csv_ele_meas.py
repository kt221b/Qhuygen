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
def save_dataset_to_csv(dataset, drive_path):
    analysis_folder = os.path.join(drive_path)
    analysis_folder = os.path.dirname(analysis_folder)
    df = dataset.to_pandas_dataframe().reset_index()
    df.to_csv(os.path.join(analysis_folder, f'dataset_{dataset.captured_run_id}_{dataset.sample_name}.csv'),
              sep=',', columns=['elm_V','elm_sense'], encoding='utf-8', index=False)
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
nID = int(input("Define nID: "))
        
#Define nID in the console as nID = 18
print("ID =", nID)


# qcodes.initialise_or_create_database_at(DB_path_maintenance)
dset = qcodes.dataset.load_by_id(nID)
data = dset.to_xarray_dataarray_dict()
name = dset.name
experiments = qcodes.experiments()

print(data)

# %%  
                                ################### DC Measurements ###############################
# %%
# IV with K6517B

voltage = data['elm_V'].data
current = data['elm_sense'].data
# save_dataset_to_csv(dset, db_file_path)
# %%
# IV with K6517B and bg with K2450

Vbg = data['sm_Source_Set_Voltage'].data
I = data['elm_sense'].data
# %%
# 4 probe with K6517B and nanovoltmeter

Vbg = data['sm_Source_Set_Voltage'].data
I = data['elm_sense'].data
# %%
                                ################### AC Measurements ###############################
#%%
#2 probe with one Zurich lockin 

# dfdc = dset.get_parameter_data('lii_X')
# AC_V_2prb = dfdc['lii_X']['lii_sigoutamp'] 

# li1_X_2prb = data['lii_X'].data
# li1_Y_2prb = data['lii_Y'].data

dfdc = dset.get_parameter_data('li1_X')
AC_V_2prb = dfdc['li1_X']['li1_sigoutamp'] 

li1_X_2prb = data['li1_X'].data
li1_Y_2prb = data['li1_Y'].data

li1_R_2prb = np.sqrt(li1_X_2prb**2 + li1_Y_2prb**2)


#%%
#2 probe with one Zurich lockin and backgate with K2450


bg_voltage_2prb= data['sm_source_voltage'].data

# li1_X_2prb_bg = data['lii_X'].data
# li1_Y_2prb_bg = data['lii_Y'].data

li1_X_2prb_bg = data['li1_X'].data
li1_Y_2prb_bg = data['li1_Y'].data

li1_R_2prb_bg = np.sqrt(li1_X_2prb_bg**2 + li1_Y_2prb_bg**2)



#%%
#4probe with two Zurich lockin (NO backgate)

AC_V_4prb= data['li1_sigoutamp'].data

li1_X_4prb = data['li1_X'].data
li1_Y_4prb = data['li1_Y'].data

li2_X_4prb = data['li2_X'].data
li2_Y_4prb = data['li2_Y'].data

li1_R_4prb = np.sqrt(li1_X_4prb**2 + li1_Y_4prb**2)
li2_R_4prb = np.sqrt(li2_X_4prb**2 + li2_Y_4prb**2)

#%%
#4probe with two Zurich lockin (constant backgate) and sweeping AC voltage 

AC_V_4prb_const_bg00 = data['li1_sigoutamp'].data


li1_R_4prb_const_bg00 = data['li1_R'].data
li2_R_4prb_const_bg00 = data['li2_R'].data
#%%
#4probe with two Zurich lockin (constant backgate) and sweeping AC voltage 

AC_V_4prb_const_bg10 = data['li1_sigoutamp'].data


li1_R_4prb_const_bg10 = data['li1_R'].data
li2_R_4prb_const_bg10 = data['li2_R'].data

#%%
#4probe with two Zurich lockin (constant backgate) and sweeping AC voltage 

AC_V_4prb_const_bg20 = data['li1_sigoutamp'].data


li1_R_4prb_const_bg20 = data['li1_R'].data
li2_R_4prb_const_bg20 = data['li2_R'].data

#%%
#4probe with two Zurich lockin (constant backgate) and sweeping AC voltage 

AC_V_4prb_const_bg30 = data['li1_sigoutamp'].data


li1_R_4prb_const_bg30 = data['li1_R'].data
li2_R_4prb_const_bg30 = data['li2_R'].data

#%%
#4probe with two Zurich lockin (constant backgate) and sweeping AC voltage 

AC_V_4prb_const_bg40 = data['li1_sigoutamp'].data


li1_R_4prb_const_bg40 = data['li1_R'].data
li2_R_4prb_const_bg40 = data['li2_R'].data

#%%
#4probe with two Zurich lockin (constant backgate) and sweeping AC voltage 

AC_V_4prb_const_bg50 = data['li1_sigoutamp'].data


li1_R_4prb_const_bg50 = data['li1_R'].data
li2_R_4prb_const_bg50 = data['li2_R'].data

#%%
#4probe with two Zurich lockin and backgate with K2450


bg_voltage_4prb= data['sm_source_voltage'].data

li1_X_4prb_bg = data['li1_X'].data
li1_Y_4prb_bg = data['li1_Y'].data

li2_X_4prb_bg = data['li2_X'].data
li2_Y_4prb_bg = data['li2_Y'].data

li1_R_4prb_bg = np.sqrt(li1_X_4prb_bg**2 + li1_Y_4prb_bg**2)
li2_R_4prb_bg = np.sqrt(li2_X_4prb_bg**2 + li2_Y_4prb_bg**2)


#%%
# 2 probe with one stanford lockin


# dfdc = dset.get_parameter_data('li1_X')
# AC_V = dfdc['li_X']['li1_amplitude'] 
AC_V = data['li_amplitude'].data 
li_X_2prb = data['li_X'].data
li_Y_2prb = data['li_Y'].data
li_R_2prb = data['li_R'].data

#%%
# 2 probe with one stanford lockin and k2450 for backgate sweep


# dfdc = dset.get_parameter_data('li_X')
# AC_V = dfdc['li_X']['sm1_source_Set_Voltage'] 
Bg = data['sm1_Source_Set_Voltage'].data 
li_X_2prb = data['li_X'].data
li_Y_2prb = data['li_Y'].data
li_R_2prb = data['li_R'].data

# %%
# Export data

# %%  

def Export_to_txt_dc(mode = 'IV'):
    
    # parent_dir = 'H:\\My Drive\\Experiments\\Materials\\WSe2\\WSe2_LUMPY_TEkhagesh\\device_4\\measurements'
    # db_file_path = db_file_path 
    
    if mode == 'IV':
        # Path
        normalized_path = os.path.normpath(db_file_path)
        path = os.path.dirname(normalized_path)
        path1 = os.path.join(path, str(nID) + name)
        os.makedirs(path1, exist_ok=True)
        # save_dataset_to_csv(dset, path1)
        
        df = dset.to_pandas_dataframe().reset_index()
        df.to_csv(os.path.join(path1, f'dataset_{dset.captured_run_id}_{dset.sample_name}.csv'),
                  sep=',', columns=['elm_V','elm_sense'], encoding='utf-8', index=False)

        
    if mode =='IV_bg':
        normalized_path = os.path.normpath(db_file_path)
        path = os.path.dirname(normalized_path)
        path1 = os.path.join(path, str(nID) + name)
        os.makedirs(path1, exist_ok=True)
        # save_dataset_to_csv(dset, path1)
        
        df = dset.to_pandas_dataframe().reset_index()
        df.to_csv(os.path.join(path1, f'dataset_{dset.captured_run_id}_{dset.sample_name}.csv'),
                  sep=',', columns=['sm_Source_Set_Voltage_Vbg','elm_sense'], encoding='utf-8', index=False)
        
    if mode =='4probe':
        normalized_path = os.path.normpath(db_file_path)
        path = os.path.dirname(normalized_path)
        path1 = os.path.join(path, str(nID) + name)
        os.makedirs(path1, exist_ok=True)
        # save_dataset_to_csv(dset, path1)
        
        df = dset.to_pandas_dataframe().reset_index()
        df.to_csv(os.path.join(path1, f'dataset_{dset.captured_run_id}_{dset.sample_name}.csv'),
                  sep=',', columns=['sm_Source_Set_Voltage_Vbg','elm_sense'], encoding='utf-8', index=False)
# %%
# Export data

def Export_to_txt_ac(mode = '2Prb'):
    
    parent_dir = 'H:\\My Drive\\Experiments\\Materials\\WSe2\\WSe2_LUMPY_TEkhagesh\\device_4\\measurements'
    
    if mode == '2prb':
        nIDstr = str(nID) + '_' + name

        # Path
        path = os.path.join(parent_dir, nIDstr)
        os.mkdir(path)

        df = pd.DataFrame(AC_V_2prb).T
        file_name = '{}/AC_V_nID{}.txt'.format(path, nID)
        df.to_csv(file_name, sep=';', encoding='utf-8', index = False)

        df1 = pd.DataFrame(li1_R_2prb).T
        file_name1 = '{}/li1_R_2prb_nID{}.txt'.format(path, nID)
        df1.to_csv(file_name1, sep=';', encoding='utf-8', index = False)
       
    if mode =='2prb_bg':
        nIDstr = str(nID) + '_' + name

        # Path
        path = os.path.join(parent_dir, nIDstr)
        os.mkdir(path)

        df = pd.DataFrame(bg_voltage_2prb).T
        file_name2 = '{}/bg_V_2prb_bg_nID{}.txt'.format(path, nID)
        df.to_csv(file_name2, sep=';', encoding='utf-8', index = False)

        df1 = pd.DataFrame(li1_R_2prb_bg).T
        file_name1 = '{}/li1_R_2prb_bg_nID{}.txt'.format(path, nID)
        df1.to_csv(file_name1, sep=';', encoding='utf-8', index = False)

        
    if mode =='4prb':
        nIDstr = str(nID) + '_' + name

        # Path
        path = os.path.join(parent_dir, nIDstr)
        os.mkdir(path)

        df = pd.DataFrame(AC_V_4prb).T
        file_name = '{}/AC_V_nID{}.txt'.format(path, nID)
        df.to_csv(file_name, sep=';', encoding='utf-8', index = False)
        
        df1 = pd.DataFrame(li1_R_4prb).T
        file_name = '{}/li1_R_4prb_nID{}.txt'.format(path, nID)
        df1.to_csv(file_name, sep=';', encoding='utf-8', index = False)

        df2 = pd.DataFrame(li2_R_4prb).T
        file_name1 = '{}/li2_R_4prb_nID{}.txt'.format(path, nID)
        df2.to_csv(file_name1, sep=';', encoding='utf-8', index = False)
        
    if mode == '4prb_bg':
        nIDstr = str(nID) + '_' + name

        # Path
        path = os.path.join(parent_dir, nIDstr)
        os.mkdir(path)

        df = pd.DataFrame(bg_voltage_4prb).T
        file_name2 = '{}/bg_V_4prb_bg_nID{}.txt'.format(path, nID)
        df.to_csv(file_name2, sep=';', encoding='utf-8', index = False)
         
        df1 = pd.DataFrame(li1_R_4prb_bg).T
        file_name = '{}/li1_R_4prb_bg_nID{}.txt'.format(path, nID)
        df1.to_csv(file_name, sep=';', encoding='utf-8', index = False)

        df2 = pd.DataFrame(li2_R_4prb_bg).T
        file_name1 = '{}/li2_R_4prb_bg_nID{}.txt'.format(path, nID)
        df2.to_csv(file_name1, sep=';', encoding='utf-8', index = False)
    
    
    if mode == '4prb_const_bg00':
        nIDstr = str(nID) + '_const_bg'

        # Path
        path = os.path.join(parent_dir, nIDstr)
        os.mkdir(path)

        df = pd.DataFrame(AC_V_4prb_const_bg00).T
        file_name2 = '{}/AC_V_4prb_const_bg00_nID{}.txt'.format(path, nID)
        df.to_csv(file_name2, sep=';', encoding='utf-8', index = False)
         
        df1 = pd.DataFrame(li1_R_4prb_const_bg00).T
        file_name = '{}/li1_R_4prb_const_bg00_nID{}.txt'.format(path, nID)
        df1.to_csv(file_name, sep=';', encoding='utf-8', index = False)

        df2 = pd.DataFrame(li2_R_4prb_const_bg00).T
        file_name1 = '{}/li2_R_4prb_const_bg00_nID{}.txt'.format(path, nID)
        df2.to_csv(file_name1, sep=';', encoding='utf-8', index = False)
        
    if mode == '4prb_const_bg10':
        nIDstr = str(nID) + '_const_bg'

        # Path
        path = os.path.join(parent_dir, nIDstr)
        os.mkdir(path)

        df = pd.DataFrame(AC_V_4prb_const_bg10).T
        file_name2 = '{}/AC_V_4prb_const_bg10_nID{}.txt'.format(path, nID)
        df.to_csv(file_name2, sep=';', encoding='utf-8', index = False)
         
        df1 = pd.DataFrame(li1_R_4prb_const_bg10).T
        file_name = '{}/li1_R_4prb_const_bg10_nID{}.txt'.format(path, nID)
        df1.to_csv(file_name, sep=';', encoding='utf-8', index = False)

        df2 = pd.DataFrame(li2_R_4prb_const_bg10).T
        file_name1 = '{}/li2_R_4prb_const_bg10_nID{}.txt'.format(path, nID)
        df2.to_csv(file_name1, sep=';', encoding='utf-8', index = False)
  
    if mode == '4prb_const_bg20':
        nIDstr = str(nID) + '_const_bg'

        # Path
        path = os.path.join(parent_dir, nIDstr)
        os.mkdir(path)

        df = pd.DataFrame(AC_V_4prb_const_bg20).T
        file_name2 = '{}/AC_V_4prb_const_bg20_nID{}.txt'.format(path, nID)
        df.to_csv(file_name2, sep=';', encoding='utf-8', index = False)
         
        df1 = pd.DataFrame(li1_R_4prb_const_bg20).T
        file_name = '{}/li1_R_4prb_const_bg20_nID{}.txt'.format(path, nID)
        df1.to_csv(file_name, sep=';', encoding='utf-8', index = False)

        df2 = pd.DataFrame(li2_R_4prb_const_bg20).T
        file_name1 = '{}/li2_R_4prb_const_bg20_nID{}.txt'.format(path, nID)
        df2.to_csv(file_name1, sep=';', encoding='utf-8', index = False) 

    if mode == '4prb_const_bg30':
        nIDstr = str(nID) + '_const_bg'

        # Path
        path = os.path.join(parent_dir, nIDstr)
        os.mkdir(path)

        df = pd.DataFrame(AC_V_4prb_const_bg30).T
        file_name2 = '{}/AC_V_4prb_const_bg30_nID{}.txt'.format(path, nID)
        df.to_csv(file_name2, sep=';', encoding='utf-8', index = False)
         
        df1 = pd.DataFrame(li1_R_4prb_const_bg30).T
        file_name = '{}/li1_R_4prb_const_bg30_nID{}.txt'.format(path, nID)
        df1.to_csv(file_name, sep=';', encoding='utf-8', index = False)

        df2 = pd.DataFrame(li2_R_4prb_const_bg30).T
        file_name1 = '{}/li2_R_4prb_const_bg30_nID{}.txt'.format(path, nID)
        df2.to_csv(file_name1, sep=';', encoding='utf-8', index = False)            
            
    if mode == '4prb_const_bg40':
        nIDstr = str(nID) + '_const_bg'

        # Path
        path = os.path.join(parent_dir, nIDstr)
        os.mkdir(path)

        df = pd.DataFrame(AC_V_4prb_const_bg40).T
        file_name2 = '{}/AC_V_4prb_const_bg40_nID{}.txt'.format(path, nID)
        df.to_csv(file_name2, sep=';', encoding='utf-8', index = False)
         
        df1 = pd.DataFrame(li1_R_4prb_const_bg40).T
        file_name = '{}/li1_R_4prb_const_bg40_nID{}.txt'.format(path, nID)
        df1.to_csv(file_name, sep=';', encoding='utf-8', index = False)

        df2 = pd.DataFrame(li2_R_4prb_const_bg40).T 
        file_name1 = '{}/li2_R_4prb_const_bg40_nID{}.txt'.format(path, nID)
        df2.to_csv(file_name1, sep=';', encoding='utf-8', index = False)            
                
    if mode == '4prb_const_bg50':
        nIDstr = str(nID) + '_const_bg'

        # Path
        path = os.path.join(parent_dir, nIDstr)
        os.mkdir(path)

        df = pd.DataFrame(AC_V_4prb_const_bg50).T
        file_name2 = '{}/AC_V_4prb_const_bg50_nID{}.txt'.format(path, nID)
        df.to_csv(file_name2, sep=';', encoding='utf-8', index = False)
         
        df1 = pd.DataFrame(li1_R_4prb_const_bg50).T
        file_name = '{}/li1_R_4prb_const_bg50_nID{}.txt'.format(path, nID)
        df1.to_csv(file_name, sep=';', encoding='utf-8', index = False)

        df2 = pd.DataFrame(li2_R_4prb_const_bg50).T
        file_name1 = '{}/li2_R_4prb_const_bg50_nID{}.txt'.format(path, nID)
        df2.to_csv(file_name1, sep=';', encoding='utf-8', index = False)
        
    if mode == '2prb_stanford':
        nIDstr = str(nID) + '_' + name

        # Path
        path = os.path.join(parent_dir, nIDstr)
        os.mkdir(path)

        df = pd.DataFrame(AC_V).T
        file_name = path + '/AC_V_2prb.csv'
        df.to_csv(file_name, sep=';', encoding='utf-8', index = False)

        df1 = pd.DataFrame(li_X_2prb).T
        file_name1 = path + '/li1_X_2prb.csv'
        df1.to_csv(file_name1, sep=';', encoding='utf-8', index = False)

        df2 = pd.DataFrame(li_Y_2prb).T
        file_name2 = path + '/li_Y_2prb.csv'
        df2.to_csv(file_name2, sep=';', encoding='utf-8', index = False)

        df3 = pd.DataFrame(li_R_2prb).T
        file_name3 = path + '/li1_R_2prb.csv'
        df3.to_csv(file_name3, sep=';', encoding='utf-8', index = False)

    elif mode == '2prb_stanford_K2450_bg':
        nIDstr = str(nID) + '_' + name

        # Path
        path = os.path.join(parent_dir, nIDstr)
        os.mkdir(path)

        df = pd.DataFrame(Bg).T
        file_name = path + '/bg_Vdc.csv'
        df.to_csv(file_name, sep=';', encoding='utf-8', index = False)

        df1 = pd.DataFrame(li_X_2prb).T
        file_name1 = path + '/li1_X_2prb.csv'
        df1.to_csv(file_name1, sep=';', encoding='utf-8', index = False)

        df2 = pd.DataFrame(li_Y_2prb).T
        file_name2 = path + '/li_Y_2prb.csv'
        df2.to_csv(file_name2, sep=';', encoding='utf-8', index = False)

        df3 = pd.DataFrame(li_R_2prb).T
        file_name3 = path + '/li1_R_2prb.csv'
        df3.to_csv(file_name3, sep=';', encoding='utf-8', index = False)


# %% plotting the graphs

parent_dir = 'H:\\My Drive\\Experiments\\Materials\\WSe2\\WSe2_LUMPY_TEkhagesh\\device_4\\measurements\\'

# nIDstr = str(nID) + '_' + name
# Path



def plot_graph(mode = '2Prb'):
    if mode == '2prb':
        path = parent_dir + str(nID) + '_' + name
        AC_V= (1/np.sqrt(2))*np.loadtxt(path +'/AC_V_nID{}.txt'.format(nID), unpack=True, delimiter=';')
        li1R= np.loadtxt(path +'/li1_R_2prb_nID{}.txt'.format(nID), unpack=True, delimiter=';')
        
        title = 'Vac_vs_Ids_{}'.format(nID)
        fig1, ax1 = plt.subplots()
        ax1.title.set_text(title)
        im1 = ax1.scatter(AC_V[:,1], li1R[:,1], s=15.0, facecolor='none', edgecolors='black')
        im1 = ax1.plot(AC_V[:,1], li1R[:,1], lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Applied AC voltge (V)', fontsize=16, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Ids (A)', fontsize=16, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', length=10, which='major')

        fig1.tight_layout()
        fig1.show()
        fig1.savefig(path + '/' + title + '.tif')
        # cbar1 = fig1.colorbar(im1, ax=axs1[0], fraction=fraction)
        
    if mode == '2prb_bg':
        path = parent_dir + str(nID) + '_' + name
        bg_V= np.loadtxt(path + '/bg_V_2prb_bg_nID{}.txt'.format(nID), unpack=True, delimiter=';')
        li1R= np.loadtxt(path +'/li1_R_2prb_bg_nID{}.txt'.format(nID), unpack=True, delimiter=';')
        
        title = 'Vbg_vs_Ids_{}'.format(nID)
        fig, ax = plt.subplots()
        ax.title.set_text(title)
        im2 = ax.scatter(bg_V[:,1], li1R[:,1], s=15.0, facecolor='none', edgecolors='black')
        im2 = ax.plot(bg_V[:,1], li1R[:,1], lw=1.0, color='black')
        ax.set_xlabel('Applied bg voltge (V)', fontsize=16, family = 'Times New Roman', color='black')  
        ax.set_ylabel('Ids (A)', fontsize=16, family = 'Times New Roman', color='black')
        # ax.set_xticklabels([])
        # ax.set_yticklabels([])
        # ax.set_xticks([])
        # ax.set_yticks([])
        
        fig.tight_layout()
        fig.show()
        fig.savefig(path + '/' + title + '.tif')
        
    if mode == '4prb':
        path = parent_dir + str(nID) + '_' + name
        AC_V= (1/np.sqrt(2))*np.loadtxt(path +'/AC_V_nID{}.txt'.format(nID), unpack=True, delimiter=';')
        li1R= np.loadtxt(path +'/li1_R_4prb_nID{}.txt'.format(nID), unpack=True, delimiter=';')
        li2R= np.loadtxt(path + '/li2_R_4prb_nID{}.txt'.format(nID), unpack=True, delimiter=';')
              
        
        title = 'Vac_vs_Ids_{}'.format(nID)
        fig, ax = plt.subplots()
        ax.title.set_text(title)
        im1 = ax.scatter(AC_V[:,1], li1R[:,1], s=15.0, facecolor='none', edgecolors='black')
        im1 = ax.plot(AC_V[:,1], li1R[:,1], lw=1.0, color='black')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax.set_xlabel('Applied AC voltge (V)', fontsize=16, family = 'Times New Roman', color='black')  
        ax.set_ylabel('Ids (A)', fontsize=16, family = 'Times New Roman', color='black')
        # ax.set_xticklabels([])
        # ax.set_yticklabels([])
        # ax.set_xticks([])
        # ax.set_yticks([])
        ax.tick_params(axis='both', length=10, which='major')
        fig.tight_layout()
        fig.show()
        fig.savefig(path + '/' + title + '.tif')
        # cbar1 = fig1.colorbar(im1, ax=axs1[0], fraction=fraction)
        
        title1 = 'Ids_vs_Vds_{}'.format(nID)
        fig1, ax1 = plt.subplots()
        ax1.title.set_text(title1)
        im4 = ax1.scatter(li1R[:,1], li2R[:,1], s=15.0, facecolor='none', edgecolors='black')
        im4 = ax1.plot(li1R[:,1], li2R[:,1], lw=1.0, color='black')
        ax1.set_xlabel('Ids (A)', fontsize=16, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Vds (V)', fontsize=16, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', length=10, which='major')
        
        fig1.tight_layout()
        fig1.show()
        fig1.savefig(path + '/' + title1 + '.tif')

        
    if mode == '4prb_bg':
        path = parent_dir + str(nID) + '_' + name
        bg_V= np.loadtxt(path + '/bg_V_4prb_bg_nID{}.txt'.format(nID), unpack=True, delimiter=';')
        li1R= np.loadtxt(path +'/li1_R_4prb_bg_nID{}.txt'.format(nID), unpack=True, delimiter=';')
        li2R= np.loadtxt(path + '/li2_R_4prb_bg_nID{}.txt'.format(nID), unpack=True, delimiter=';') 
        
        title = 'Vbg_vs_Ids_{}'.format(nID)
        fig, ax = plt.subplots()
        ax.title.set_text(title)
        im2 = ax.scatter(bg_V[:,1], li1R[:,1], s=15.0, facecolor='none', edgecolors='black')
        im2 = ax.plot(bg_V[:,1], li1R[:,1], lw=1.0, color='black')
        ax.set_xlabel('Applied bg voltge (V)', fontsize=16, family = 'Times New Roman', color='black')  
        ax.set_ylabel('Ids (A)', fontsize=16, family = 'Times New Roman', color='black')
        # ax.set_xticklabels([])
        # ax.set_yticklabels([])
        # ax.set_xticks([])
        # ax.set_yticks([])
        fig.tight_layout()
        fig.show()
        fig.savefig(path + '/' + title + '.tif')
        
        title1 = 'Vbg_vs_Vds_{}'.format(nID)
        fig1, ax1 = plt.subplots()
        ax1.title.set_text(title1)
        im4 = ax1.scatter(bg_V[2:,1], li2R[2:,1], s=15.0, facecolor='none', edgecolors='black')
        im4 = ax1.plot(bg_V[2:,1], li2R[2:,1], lw=1.0, color='black')
        ax1.set_xlabel('Applied bg voltge (V)', fontsize=16, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Vds (V)', fontsize=16, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', length=10, which='major')
        
        fig1.tight_layout()
        fig1.show()
        fig1.savefig(path + '/' + title1 + '.tif')

        
        title2 = 'Ids_vs_Vds_{}'.format(nID)
        fig2, ax2 = plt.subplots()
        ax2.title.set_text(title2)
        im3 = ax2.scatter(li1R[2:,1], li2R[2:,1], s=15.0, facecolor='none', edgecolors='black')
        im3 = ax2.plot(li1R[2:,1], li2R[2:,1], lw=1.0, color='black')
        ax2.set_xlabel('Ids (A)', fontsize=16, family = 'Times New Roman', color='black')  
        ax2.set_ylabel('Vds (V)', fontsize=16, family = 'Times New Roman', color='black')
        # ax3.set_xticklabels([])
        # ax3.set_yticklabels([])
        # ax3.set_xticks([])
        # ax3.set_yticks([])
        ax2.tick_params(axis='both', length=10, which='major')
        fig2.tight_layout()
        fig2.show()
        fig2.savefig(path + '/' + title2 + '.tif')
        
    if mode == '4prb_const_bg':
        path = parent_dir + str(nID) + '_const_bg' 
        AC_V_00= (1/np.sqrt(2))*np.loadtxt(parent_dir + str(nID) + '_const_bg' +'/AC_V_4prb_const_bg00_nID{}.txt'.format(nID), unpack=True, delimiter=';')
        li1R_00= np.loadtxt(parent_dir + str(nID) + '_const_bg' + '/li1_R_4prb_const_bg00_nID{}.txt'.format(nID), unpack=True, delimiter=';')
        li2R_00= np.loadtxt(parent_dir + str(nID) + '_const_bg' + '/li2_R_4prb_const_bg00_nID{}.txt'.format(nID), unpack=True, delimiter=';')

        
        AC_V_10= (1/np.sqrt(2))*np.loadtxt(parent_dir + str(nID+1) + '_const_bg' + '/AC_V_4prb_const_bg10_nID{}.txt'.format(nID+1), unpack=True, delimiter=';')
        li1R_10= np.loadtxt(parent_dir + str(nID+1) + '_const_bg' +'/li1_R_4prb_const_bg10_nID{}.txt'.format(nID+1), unpack=True, delimiter=';')
        li2R_10= np.loadtxt(parent_dir + str(nID+1) + '_const_bg' + '/li2_R_4prb_const_bg10_nID{}.txt'.format(nID+1), unpack=True, delimiter=';')
        
        AC_V_20= (1/np.sqrt(2))*np.loadtxt(parent_dir + str(nID+2) + '_const_bg' + '/AC_V_4prb_const_bg20_nID{}.txt'.format(nID+2), unpack=True, delimiter=';')
        li1R_20= np.loadtxt(parent_dir + str(nID+2) + '_const_bg' +'/li1_R_4prb_const_bg20_nID{}.txt'.format(nID+2), unpack=True, delimiter=';')
        li2R_20= np.loadtxt(parent_dir + str(nID+2) + '_const_bg' + '/li2_R_4prb_const_bg20_nID{}.txt'.format(nID+2), unpack=True, delimiter=';')
        
        AC_V_30= (1/np.sqrt(2))*np.loadtxt(parent_dir + str(nID+3) + '_const_bg' + '/AC_V_4prb_const_bg30_nID{}.txt'.format(nID+3), unpack=True, delimiter=';')
        li1R_30= np.loadtxt(parent_dir + str(nID+3) + '_const_bg' +'/li1_R_4prb_const_bg30_nID{}.txt'.format(nID+3), unpack=True, delimiter=';')
        li2R_30= np.loadtxt(parent_dir + str(nID+3) + '_const_bg' + '/li2_R_4prb_const_bg30_nID{}.txt'.format(nID+3), unpack=True, delimiter=';')
        
        AC_V_40= (1/np.sqrt(2))*np.loadtxt(parent_dir + str(nID+4) + '_const_bg' + '/AC_V_4prb_const_bg40_nID{}.txt'.format(nID+4), unpack=True, delimiter=';')
        li1R_40= np.loadtxt(parent_dir + str(nID+4) + '_const_bg' +'/li1_R_4prb_const_bg40_nID{}.txt'.format(nID+4), unpack=True, delimiter=';')
        li2R_40= np.loadtxt(parent_dir + str(nID+4) + '_const_bg' + '/li2_R_4prb_const_bg40_nID{}.txt'.format(nID+4), unpack=True, delimiter=';')
        
        AC_V_50= (1/np.sqrt(2))*np.loadtxt(parent_dir + str(nID+5) + '_const_bg' + '/AC_V_4prb_const_bg50_nID{}.txt'.format(nID+5), unpack=True, delimiter=';')
        li1R_50= np.loadtxt(parent_dir + str(nID+5) + '_const_bg' +'/li1_R_4prb_const_bg50_nID{}.txt'.format(nID+5), unpack=True, delimiter=';')
        li2R_50= np.loadtxt(parent_dir + str(nID+5) + '_const_bg' + '/li2_R_4prb_const_bg50_nID{}.txt'.format(nID+5), unpack=True, delimiter=';')
        


        title = 'Vac_vs_Ids_{}'.format(nID)
        fig, ax = plt.subplots()
        ax.title.set_text(title)
        im1 = ax.scatter(AC_V_00[:,1], li1R_00[:,1], s=40.0, facecolor='none', edgecolors='black')
        im1 = ax.plot(AC_V_00[:,1], li1R_00[:,1], lw=1.0, color='black', label='-0.0 V bg')
        im2 = ax.scatter(AC_V_10[:,1], li1R_10[:,1], s=40.0, facecolor='none', edgecolors='red')
        im2 = ax.plot(AC_V_10[:,1], li1R_10[:,1], lw=1.0, color='red', label='-10.0 V bg')
        im3 = ax.scatter(AC_V_20[:,1], li1R_20[:,1], s=40.0, facecolor='none', edgecolors='blue')
        im3 = ax.plot(AC_V_20[:,1], li1R_20[:,1], lw=1.0, color='blue', label='-20.0 V bg')
        im4 = ax.scatter(AC_V_30[:,1], li1R_30[:,1], s=40.0, facecolor='none', edgecolors='magenta')
        im4 = ax.plot(AC_V_30[:,1], li1R_30[:,1], lw=1.0, color='magenta', label='-30.0 V bg')
        im5 = ax.scatter(AC_V_40[:,1], li1R_40[:,1], s=40.0, facecolor='none', edgecolors='green')
        im5 = ax.plot(AC_V_40[:,1], li1R_40[:,1], lw=1.0, color='green', label='-40.0 V bg')
        im6 = ax.scatter(AC_V_50[:,1], li1R_50[:,1], s=40.0, facecolor='none', edgecolors='grey')
        im6 = ax.plot(AC_V_40[:,1], li1R_50[:,1], lw=1.0, color='grey', label='-50.0 V bg')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax.set_xlabel('Applied AC voltge (V)', fontsize=16, family = 'Times New Roman', color='black')  
        ax.set_ylabel('Ids (A)', fontsize=16, family = 'Times New Roman', color='black')
        ax.legend()
        # ax.set_xticklabels([])
        # ax.set_yticklabels([])
        # ax.set_xticks([])
        # ax.set_yticks([])
        ax.tick_params(axis='both', length=10, which='major')
        fig.tight_layout()
        fig.show()
        fig.savefig(path + '/' + title + '.tif')
        # cbar1 = fig1.colorbar(im1, ax=axs1[0], fraction=fraction)
        
        title1 = 'Vac_vs_Vds_{}'.format(nID)
        fig1, ax1 = plt.subplots()
        ax.title.set_text(title1)
        im1 = ax1.scatter(AC_V_00[:,1], li2R_00[:,1], s=40.0, facecolor='none', edgecolors='black')
        im1 = ax1.plot(AC_V_00[:,1], li2R_00[:,1], lw=1.0, color='black', label='-0.0 V bg')
        im2 = ax1.scatter(AC_V_10[:,1], li2R_10[:,1], s=40.0, facecolor='none', edgecolors='red')
        im2 = ax1.plot(AC_V_10[:,1], li2R_10[:,1], lw=1.0, color='red', label='-10.0 V bg')
        im3 = ax1.scatter(AC_V_20[:,1], li2R_20[:,1], s=40.0, facecolor='none', edgecolors='blue')
        im3 = ax1.plot(AC_V_20[:,1], li2R_20[:,1], lw=1.0, color='blue', label='-20.0 V bg')
        im4 = ax1.scatter(AC_V_30[:,1], li2R_30[:,1], s=40.0, facecolor='none', edgecolors='magenta')
        im4 = ax1.plot(AC_V_30[:,1], li2R_30[:,1], lw=1.0, color='magenta', label='-30.0 V bg')
        im5 = ax1.scatter(AC_V_40[:,1], li2R_40[:,1], s=40.0, facecolor='none', edgecolors='green')
        im5 = ax1.plot(AC_V_40[:,1], li2R_40[:,1], lw=1.0, color='green', label='-40.0 V bg')
        im6 = ax1.scatter(AC_V_50[:,1], li2R_50[:,1], s=40.0, facecolor='none', edgecolors='grey')
        im6 = ax1.plot(AC_V_50[:,1], li2R_50[:,1], lw=1.0, color='grey', label='-50.0 V bg')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Applied AC voltge (V)', fontsize=16, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Vds (A)', fontsize=16, family = 'Times New Roman', color='black')
        ax1.legend()
        # ax.set_xticklabels([])
        # ax.set_yticklabels([])
        # ax.set_xticks([])
        # ax.set_yticks([])
        ax1.tick_params(axis='both', length=10, which='major')
        fig1.tight_layout()
        fig1.show()
        fig1.savefig(path + '/' + title1 + '.tif')
        # cbar1 = fig1.colorbar(im1, ax=axs1[0], fraction=fraction)
        
        
        title2 = 'Ids_vs_Vds_{}'.format(nID)
        fig2, ax2 = plt.subplots()
        ax2.title.set_text(title2)
        im1 = ax2.scatter(li1R_00[:,1], li2R_00[:,1], s=40.0, facecolor='none', edgecolors='black')
        im1 = ax2.plot(li1R_00[:,1], li2R_00[:,1], lw=1.0, color='black', label='-0.0 V bg')
        im2 = ax2.scatter(li1R_10[:,1], li2R_10[:,1], s=40.0, facecolor='none', edgecolors='red')
        im2 = ax2.plot(li1R_10[:,1], li2R_10[:,1], lw=1.0, color='red', label='-10.0 V bg')
        im3 = ax2.scatter(li1R_20[:,1], li2R_20[:,1], s=40.0, facecolor='none', edgecolors='blue')
        im3 = ax2.plot(li1R_20[:,1], li2R_20[:,1], lw=1.0, color='blue', label='-20.0 V bg')
        im4 = ax2.scatter(li1R_30[:,1], li2R_30[:,1], s=40.0, facecolor='none', edgecolors='magenta')
        im4 = ax2.plot(li1R_30[:,1], li2R_30[:,1], lw=1.0, color='magenta', label='-30.0 V bg')
        im5 = ax2.scatter(li1R_40[:,1], li2R_40[:,1], s=40.0, facecolor='none', edgecolors='green')
        im5 = ax2.plot(li1R_40[:,1], li2R_40[:,1], lw=1.0, color='green', label='-40.0 V bg')
        im6 = ax2.scatter(li1R_50[:,1], li2R_50[:,1], s=40.0, facecolor='none', edgecolors='grey')
        im6 = ax2.plot(li1R_50[:,1], li2R_50[:,1], lw=1.0, color='grey', label='-50.0 V bg')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax2.set_xlabel('Ids (A)', fontsize=16, family = 'Times New Roman', color='black')  
        ax2.set_ylabel('Vds (V)', fontsize=16, family = 'Times New Roman', color='black')
        ax2.legend()
        # ax.set_xticklabels([])
        # ax.set_yticklabels([])
        # ax.set_xticks([])
        # ax.set_yticks([])
        ax2.tick_params(axis='both', length=10, which='major')
        fig2.tight_layout()
        fig2.show()
        fig2.savefig(path + '/' + title2+ '.tif', dpi=300)
        # cbar1 = fig1.colorbar(im1, ax=axs1[0], fraction=fraction)

    elif mode == '2prb_stanford':
        path = parent_dir + str(nID) + '_' + name
        AC_V= np.loadtxt(path + '/AC_V_2prb.csv', unpack=True, delimiter=';')
        liR= np.loadtxt(path +'/li1_R_2prb.csv', unpack=True, delimiter=';')

        
        title = 'Vac_vs_Current_{}'.format(nID)
        fig, ax = plt.subplots()
        ax.title.set_text(title)
        im2 = ax.scatter(AC_V[:,1], liR[:,1]*1000, s=15.0, facecolor='none', edgecolors='black')
        im2 = ax.plot(AC_V[:,1], liR[:,1]*1000, lw=1.0, color='black')
        ax.set_xlabel('AC voltge (V)', fontsize=28, family = 'Times New Roman', color='black')  
        ax.set_ylabel('Current (A)', fontsize=28, family = 'Times New Roman', color='black')
        # ax.set_xticklabels([])
        # ax.set_yticklabels([])
        # ax.set_xticks([])
        # ax.set_yticks([])
        ax.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
        ax.tick_params(axis='both', length=10, which='major')
        fig.tight_layout()
        fig.show()
        fig.savefig(path + '/' + title + '.png', dpi=300)
        
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
    
    
    elm_V = data.get_parameter_data('elm_V')['elm_V']['elm_V']
    elm_sense = data.get_parameter_data('elm_sense')['elm_sense']['elm_sense']*1e12
    
    try:
        Vbg = data.get_parameter_data('sm1_Source_Set_Voltage')['sm1_Source_Set_Voltage']['sm1_Source_Set_Voltage']
    except:
        pass
    
    Vbg =Vbg[::2] 
    
    if  mode== 'IV_K6517B':
        fig, ax = plt.subplots()
        # fig , axs = plt.subplots(1,1, sharex=True, figsize=(11,7))
        c1 = "#D60000"
        c2 = "#0000FF"
        color = color_gradient(c1, c2, len(elm_V))
        normalized_path = os.path.normpath(db_file_path)
        path = os.path.dirname(normalized_path)
        path = os.path.join(path, str(run_id))
        os.mkdir(path)
        
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

    if  mode== 'IVg_K2450_K6517B':
        fig, ax = plt.subplots()
        # fig , axs = plt.subplots(1,1, sharex=True, figsize=(11,7))
        c1 = "#D60000"
        c2 = "#0000FF"
        color = color_gradient(c1, c2, len(Vbg))
        normalized_path = os.path.normpath(db_file_path)
        path = os.path.dirname(normalized_path)
        path = os.path.join(path, str(run_id))
        os.mkdir(path)
        
        im1 = ax.scatter(Vbg, elm_sense, s=10, color = color)
        im1 = ax.plot(Vbg, elm_sense, lw=1.0, color='black')
        ax.set_title('IVg_K2450_K6517B')
        ax.set_xlabel('V_bg (Volts)', fontsize=20, family = 'Arial', color='black')  
        ax.set_ylabel('I_ds (pA)', fontsize=20, family = 'Arial', color='black')
        ax.xaxis.set_major_locator(MaxNLocator(nbins=10))
        # ax.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
        
        # axs[1,0].axis('off')
        # axs[0,1].axis('off')
        # axs[1,1].axis('off')
        
        
        fig.tight_layout()
        fig.savefig(path + '/' + 'ID' + str(run_id) +'.png')