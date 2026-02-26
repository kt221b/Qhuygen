# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 12:16:37 2023

@author: Jaume Meseguer

Code made to plot LD Scans
"""
import qcodes
import os
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
nID = int(input("Define nID: "))
        
#Define nID in the console as nID = 18
print("ID =", nID)


# qcodes.initialise_or_create_database_at(DB_path_maintenance)
scan = 'y'
dset = qcodes.dataset.load_by_id(nID)
data = dset.to_xarray_dataarray_dict()
name = dset.name
experiments = qcodes.experiments()

print(data)

# %%
# MOKE
dcx = data['dcli_ch1_databuffer'].data
f2x = data['f2li_ch1_databuffer'].data
f1x = data['f1li_ch1_databuffer'].data


f2x = np.array([f2x[i, ~np.isnan(f2x[i,:])] for i in range(f2x.shape[0])])
f1x = np.array([f1x[i, ~np.isnan(f1x[i,:])] for i in range(f1x.shape[0])])
dcx = np.array([dcx[i, ~np.isnan(dcx[i,:])] for i in range(dcx.shape[0])])

Kerr = (f2x/dcx)
RMCD = (f1x/dcx)

# %%
# BFP

dfdc = dset.get_parameter_data('dcli_X')
BFPx = dfdc['dcli_X']['BFPx_angle'] 
BFPy = dfdc['dcli_X']['BFPy_angle'] 

# BFPx = data['BFPx_angle'].data
# BFPy = data['BFPy_angle'].data

dcx = data['dcli_X'].data
f2x = data['f2li_X'].data
f1x = data['f1li_X'].data

f2x = np.array([f2x[i, ~np.isnan(f2x[i,:])] for i in range(f2x.shape[0])])
f1x = np.array([f1x[i, ~np.isnan(f1x[i,:])] for i in range(f1x.shape[0])])
dcx = np.array([dcx[i, ~np.isnan(dcx[i,:])] for i in range(dcx.shape[0])])

BFPx = np.unique(BFPx)
BFPy = np.unique(BFPy)


Kerr = (f2x/dcx)
RMCD = (f1x/dcx)

# %%
# point_by_point_scan

dcx = data['dcli_X'].data
f2x = data['f2li_X'].data
f1x = data['f1li_X'].data

f2x = np.array([f2x[i, ~np.isnan(f2x[i,:])] for i in range(f2x.shape[0])])
f1x = np.array([f1x[i, ~np.isnan(f1x[i,:])] for i in range(f1x.shape[0])])
dcx = np.array([dcx[i, ~np.isnan(dcx[i,:])] for i in range(dcx.shape[0])])


Kerr = (f2x/dcx)
RMCD = (f1x/dcx)

# %%
# MOKE montana
dcx = data['dcli_dcli_buffer_X'].data
f1x = data['f1li_f1li_buffer_X'].data
f2x = data['f2li_f2li_buffer_X'].data


f2x = np.array([f2x[i, ~np.isnan(f2x[i,:])] for i in range(f2x.shape[0])])
f1x = np.array([f1x[i, ~np.isnan(f1x[i,:])] for i in range(f1x.shape[0])])
dcx = np.array([dcx[i, ~np.isnan(dcx[i,:])] for i in range(dcx.shape[0])])

Kerr = (f2x/dcx)
RMCD = (f1x/dcx)

# %%
#Montana 
#BFP
dfdc = dset.get_parameter_data('dcli_dcli_buffer_X')
# BFPx = dfdc['dcli_X']['BFPx_angle'] 
BFPy = dfdc['dcli_dcli_buffer_X']['bfmotory_axis_pos'] 
BFPx= np.linspace(1,499,499)

dcx = data['dcli_dcli_buffer_X'].data
f1x = data['f1li_f1li_buffer_X'].data
f2x = data['f2li_f2li_buffer_X'].data

f2x = np.array([f2x[i, ~np.isnan(f2x[i,:])] for i in range(f2x.shape[0])])
f1x = np.array([f1x[i, ~np.isnan(f1x[i,:])] for i in range(f1x.shape[0])])
dcx = np.array([dcx[i, ~np.isnan(dcx[i,:])] for i in range(dcx.shape[0])])


BFPy = np.unique(BFPy)


Kerr = (f2x/dcx)
RMCD = (f1x/dcx)
#%%
def Export_data_to_csv(mode = 'LD'):
    if mode == 'LD':
        normalized_path = os.path.normpath(db_file_path)
        path = os.path.dirname(normalized_path)
        nIDstr = str(nID) + '_' + name

        # Path
        path = os.path.join(path, nIDstr)
        os.mkdir(path)

        df = pd.DataFrame(Kerr).T
        file_name = path + '/LD.csv'
        df.to_csv(file_name, sep=';', encoding='utf-8', index = False)

        df1 = pd.DataFrame(dcx).T
        file_name1 = path + '/DC.csv'
        df1.to_csv(file_name1, sep=';', encoding='utf-8', index = False)

        df2 = pd.DataFrame(f2x).T
        file_name2 = path + '/f2.csv'
        df2.to_csv(file_name2, sep=';', encoding='utf-8', index = False)

    if mode == 'BFP':
        normalized_path = os.path.normpath(db_file_path)
        path = os.path.dirname(normalized_path)
        nIDstr = str(nID) + '_' + name
        
        # Path
        path = os.path.join(path, nIDstr)
        os.mkdir(path)


        df = pd.DataFrame(Kerr).T
        file_name = path + '/Kerr.csv'
        df.to_csv(file_name, sep=';', encoding='utf-8', index = False)
        
        df1 = pd.DataFrame(RMCD).T
        file_name1 = path + '/RMCD.csv'
        df1.to_csv(file_name1, sep=';', encoding='utf-8', index = False)
        
        df2 = pd.DataFrame(dcx).T
        file_name2 = path + '/DC.csv'
        df2.to_csv(file_name2, sep=';', encoding='utf-8', index = False)

        df3 = pd.DataFrame(f1x).T
        file_name3 = path + '/f1.csv'
        df3.to_csv(file_name3, sep=';', encoding='utf-8', index = False)

        df4 = pd.DataFrame(f2x).T
        file_name4 = path + '/f2.csv'
        df4.to_csv(file_name4, sep=';', encoding='utf-8', index = False)

        df5 = pd.DataFrame(BFPx).T
        file_name5 = path + '/BFPx.csv'
        df5.to_csv(file_name5, sep=';', encoding='utf-8', index = False)-4
        
        df6 = pd.DataFrame(BFPy).T
        file_name6 = path + '/BFPy.csv'
        df6.to_csv(file_name6, sep=';', encoding='utf-8', index = False)

    elif mode == 'MOKE':
        
        
        normalized_path = os.path.normpath(db_file_path)
        path = os.path.dirname(normalized_path)
        nIDstr = str(nID) + '_' + name
        
        # Path
        path = os.path.join(path, nIDstr)
        os.mkdir(path)

        df = pd.DataFrame(Kerr).T
        file_name = path + '/Kerr.csv'
        df.to_csv(file_name, sep=';', encoding='utf-8', index = False)

        df1 = pd.DataFrame(RMCD).T
        file_name1 = path + '/RMCD.csv'
        df1.to_csv(file_name1, sep=';', encoding='utf-8', index = False)

        df2 = pd.DataFrame(f2x).T
        file_name2 = path + '/f2.csv'
        df2.to_csv(file_name2, sep=';', encoding='utf-8', index = False)

        df3 = pd.DataFrame(f1x).T
        file_name3 = path + '/f1.csv'
        df3.to_csv(file_name3, sep=';', encoding='utf-8', index = False)

        df4 = pd.DataFrame(dcx).T
        file_name4 = path + '/DC.csv'
        df4.to_csv(file_name4, sep=';', encoding='utf-8', index = False)
#