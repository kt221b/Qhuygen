# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 12:41:37 2024

@author: Principal
"""



# import qcodes
import os
import json
import h5py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib
import csv
# matplotlib.use('Qt5Agg')
# from roipoly import MultiRoi, RoiPoly
# from skimage import data, color, io
# from qcodes import initialise_or_create_database_at, load_by_id
# from qcodes.dataset import plot_dataset


# data_MT_ZFC10 = pd.read_csv('G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh\\NiBr2_CVD_flake_Par_ZFC10Oe.dat', skiprows=47)
# data_MT_ZFC100 = pd.read_csv('G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh\\NiBr2_CVD_flake_Perp_ZFC100Oe.dat', skiprows=47)
# data_MT_FC100 = pd.read_csv('G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh\\NiBr2_CVD_flake_Perp_FC100Oe.dat', skiprows=47)
# data_MT_FC1000 = pd.read_csv('G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh\\NiBr2_CVD_flake_Perp_FC1000Oe.dat', skiprows=47)
# data_MT_FC1000 = pd.read_csv('G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh\\NiBr2_CVD_flake_Par_FC1000Oe.dat', skiprows=47)
# data_MH2K = pd.read_csv('G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh\\NiBr2_CVD_flake_Perp_MH2K.dat', skiprows=47)
# data_MH30K = pd.read_csv('G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh\\NiBr2_CVD_flake_Perp_MH30K.dat', skiprows=47)
# data_MH45K = pd.read_csv('G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh\\NiBr2_CVD_flake_Perp_MH45K.dat', skiprows=47)
# data_MH55K = pd.read_csv('G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh\\NiBr2_CVD_flake_Perp_MH55K.dat', skiprows=47)
# data_MH100K = pd.read_csv('G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh\\NiBr2_CVD_flake_Perp_MH100K.dat', skiprows=47)
# data_MH200K = pd.read_csv('G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh\\NiBr2_CVD_flake_Perp_MH200K.dat', skiprows=47)
# data_MH300K = pd.read_csv('G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh\\NiBr2_CVD_flake_Perp_MH300K.dat', skiprows=47)
# data_MH2Ka = pd.read_csv('G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_parallel_khagesh\\NiBr2_CVD_flake_Par_MH2K.dat', skiprows=47)
# data_MH250K = pd.read_csv('G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_parallel_khagesh\\NiBr2_CVD_flake_Par_MH55K.dat', skiprows=47)
# data_MH300K = pd.read_csv('G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_parallel_khagesh\\NiBr2_CVD_flake_Par_MH55K.dat', skiprows=47)

#5T Squid machine

# data_MT_ZFC10 = pd.read_csv('G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\Jaume_experiments\\NiBr2_par_H_ZFC10Oe.dat', skiprows=33)
# data_MT_FC10 = pd.read_csv('G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\Jaume_experiments\\NiBr2_par_H_FC10Oe.dat', skiprows=33)
data_MH2K = pd.read_csv('G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\Jaume_experiments\\NiBr2_par_H_MH2K.dat', skiprows=33)
# Split the data string by commas
# data_list = data.split(',')

# Replace empty strings with None
# data_list_MT = [None if x == '' else x for x in data_MT]
# data_list_MH2K = [None if x == '' else x for x in data_MH2K]
# data_list_MH30K = [None if x == '' else x for x in data_MH30K]
# Import the csv module to handle CSV operations


# # Define the output CSV file name
# output_file = 'output.csv'

# Write the data to a CSV file
# with open(output_file, mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(data_list_MT)
    
    
# df = pd.read_csv('output.csv', header=None)
# df.replace({None: np.nan}, inplace=True)
# print(df)

#%%
#for 5Tesla SQUID
# field_MT_ZFC = data_MT_ZFC.iloc[:,2]
# field_MT_FC = data_MT_FC.iloc[:,2]
field_MH2K = data_MH2K.iloc[:,2]
# field_MH30K = data_MH30K.iloc[:,2]

# temperature_MT_ZFC10 = data_MT_ZFC10.iloc[:,3]
# temperature_MT_FC10 = data_MT_FC10.iloc[:,3]

# magnetic_moment_MT_ZFC10 = data_MT_ZFC10.iloc[:,4]
# magnetic_moment_MT_FC10 = data_MT_FC10.iloc[:,4]

magnetic_moment_MH2K = data_MH2K.iloc[:,4]
# magnetic_moment_MH30K = data_MH30K.iloc[:,4]
#%%
#for 7Tesla SQUID
# field_MT_ZFC10 = data_MT_ZFC10.iloc[:,3]
# field_MT_FC10 = data_MT_FC10.iloc[:,3]

# temperature_MT_ZFC10 = data_MT_ZFC10.iloc[:,2]
# temperature_MT_FC10 = data_MT_FC10.iloc[:,2]
# temperature_MT_ZFC100 = data_MT_ZFC100.iloc[:,2]
# temperature_MT_FC100 = data_MT_FC100.iloc[:,2]
# temperature_MT_FC1000 = data_MT_FC1000.iloc[:,2]

# # magnetic_moment_MT_ZFC10 = data_MT_ZFC10.iloc[:,58]
# # magnetic_moment_MT_FC10 = data_MT_FC10.iloc[:,58]
# magnetic_moment_MT_ZFC100 = data_MT_ZFC100.iloc[:,58]
# magnetic_moment_MT_FC100 = data_MT_FC100.iloc[:,58]
# magnetic_moment_MT_FC1000 = data_MT_FC1000.iloc[:,58]

field_MH2K = data_MH2K.iloc[:,3]
field_MH2Ka = data_MH2Ka.iloc[:,3]
# field_MH30K = data_MH30K.iloc[:,3]
# field_MH45K = data_MH45K.iloc[:,3]
# field_MH55K = data_MH55K.iloc[:,3]
# field_MH100K = data_MH100K.iloc[:,3]
# field_MH200K = data_MH200K.iloc[:,3]
# field_MH300K = data_MH300K.iloc[:,3]
# # field_MH200K = data_MH55K.iloc[:,3]
# # field_MH250K = data_MH55K.iloc[:,3]
# # field_MH300K = data_MH55K.iloc[:,3]

magnetic_moment_MH2K = data_MH2K.iloc[:,58]
magnetic_moment_MH2Ka = data_MH2Ka.iloc[:,58]
# magnetic_moment_MH30K = data_MH30K.iloc[:,58]
# magnetic_moment_MH45K = data_MH45K.iloc[:,58]
# magnetic_moment_MH55K = data_MH55K.iloc[:,58]
# # magnetic_moment_MH65K = data_MH65K.iloc[:,58]
# magnetic_moment_MH100K = data_MH100K.iloc[:,58]
# magnetic_moment_MH200K = data_MH200K.iloc[:,58]
# magnetic_moment_MH300K = data_MH300K.iloc[:,58]
# # magnetic_moment_MH250K = data_MH55K.iloc[:,58]
# # magnetic_moment_MH300K = data_MH65K.iloc[:,58]
#for 7Tesla SQUID

#%%

def plot_graph(mode = 'MT'):
    if mode == 'MT':
        path = 'G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\Jaume_experiments'
        # Hz_field= np.loadtxt(path +'/Hz_field.csv'.format(nID), unpack=True, delimiter=';')
        # Hz_field1 = Hz_field[::50]
        # DC= np.loadtxt(path +'/DC.csv'.format(nID), unpack=True, delimiter=';')
        # DC1 = DC[::50]
        title = 'M_vs_T{}'.format(mode)
        fig1, ax1 = plt.subplots()
        # ax1.title.set_text(title)
        # c1 = "#D60000"
        # c2 = "#0000FF"

        # color = color_gradient(c1, c2, len(Hz_field1[:,1]))
        
        # im1 = ax1.scatter(temperature_MT_ZFC10, magnetic_moment_MT_ZFC10, s= 60, facecolors='none', edgecolors='black')
        # im1 = ax1.plot(temperature_MT_ZFC10, magnetic_moment_MT_ZFC10, lw=2.0, color='red')
        
        im1 = ax1.scatter(temperature_MT_FC10, magnetic_moment_MT_FC10, s= 60, facecolors='none', edgecolors='blue')
        im1 = ax1.plot(temperature_MT_FC10, magnetic_moment_MT_FC10, lw=2.0, color='red')
        
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Temperature (K)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Mag_Moment (emu)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.tif')


    if mode == 'MH_2K':
        path = 'G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\Jaume_experiments'
        # Hz_field= np.loadtxt(path +'/Hz_field.csv'.format(nID), unpack=True, delimiter=';')
        # Hz_field1 = Hz_field[::50]
        # DC= np.loadtxt(path +'/DC.csv'.format(nID), unpack=True, delimiter=';')
        # DC1 = DC[::50]
        title = 'M_vs_H1{}'.format(mode)
        fig1, ax1 = plt.subplots()
        # ax1.title.set_text(title)
        # c1 = "#D60000"
        # c2 = "#0000FF"

        # color = color_gradient(c1, c2, len(Hz_field1[:,1]))
        im1 = ax1.scatter(field_MH2K/10000, magnetic_moment_MH2K, s= 80, facecolors='none', edgecolors='blue')
        im1 = ax1.plot(field_MH2K/10000, magnetic_moment_MH2K, lw=2.0, color='red')
        
        # im1 = ax1.scatter(field_MH2Ka/10000, magnetic_moment_MH2Ka, s= 80, facecolors='none', edgecolors='black')
        # im1 = ax1.plot(field_MH2Ka/10000, magnetic_moment_MH2Ka, lw=2.0, color='red')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Field (Tesla)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Mag_Moment (emu)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.tif')


    if mode == 'MH_30K':
        path = 'G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh'
        # Hz_field= np.loadtxt(path +'/Hz_field.csv'.format(nID), unpack=True, delimiter=';')
        # Hz_field1 = Hz_field[::50]
        # DC= np.loadtxt(path +'/DC.csv'.format(nID), unpack=True, delimiter=';')
        # DC1 = DC[::50]
        title = 'M_vs_H{}'.format(mode)
        fig1, ax1 = plt.subplots()
        # ax1.title.set_text(title)
        # c1 = "#D60000"
        # c2 = "#0000FF"

        # color = color_gradient(c1, c2, len(Hz_field1[:,1]))
        
        im1 = ax1.scatter(field_MH30K/10000, magnetic_moment_MH30K, s= 80, facecolors='none', edgecolors='black')
        im1 = ax1.plot(field_MH30K/10000, magnetic_moment_MH30K, lw=2.0, color='red')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Field (Tesla)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Mag_Moment (emu)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.tif')
        
    if mode == 'MH_45K':
        path = 'G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh'
        # Hz_field= np.loadtxt(path +'/Hz_field.csv'.format(nID), unpack=True, delimiter=';')
        # Hz_field1 = Hz_field[::50]
        # DC= np.loadtxt(path +'/DC.csv'.format(nID), unpack=True, delimiter=';')
        # DC1 = DC[::50]
        title = 'M_vs_H{}'.format(mode)
        fig1, ax1 = plt.subplots()
        # ax1.title.set_text(title)
        # c1 = "#D60000"
        # c2 = "#0000FF"

        # color = color_gradient(c1, c2, len(Hz_field1[:,1]))
        
        im1 = ax1.scatter(field_MH45K/10000, magnetic_moment_MH45K, s= 80, facecolors='none', edgecolors='black')
        im1 = ax1.plot(field_MH45K/10000, magnetic_moment_MH45K, lw=2.0, color='red')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Field (Tesla)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Mag_Moment (emu)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.tif')
        
    if mode == 'MH_55K':
        path = 'G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh'
        # Hz_field= np.loadtxt(path +'/Hz_field.csv'.format(nID), unpack=True, delimiter=';')
        # Hz_field1 = Hz_field[::50]
        # DC= np.loadtxt(path +'/DC.csv'.format(nID), unpack=True, delimiter=';')
        # DC1 = DC[::50]
        title = 'M_vs_H{}'.format(mode)
        fig1, ax1 = plt.subplots()
        # ax1.title.set_text(title)
        # c1 = "#D60000"
        # c2 = "#0000FF"

        # color = color_gradient(c1, c2, len(Hz_field1[:,1]))
        
        im1 = ax1.scatter(field_MH55K/10000, magnetic_moment_MH55K, s= 80, facecolors='none', edgecolors='black')
        im1 = ax1.plot(field_MH55K/10000, magnetic_moment_MH55K, lw=2.0, color='red')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Field (Tesla)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Mag_Moment (emu)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.tif')

    if mode == 'MH_65K':
        path = 'G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh'
        # Hz_field= np.loadtxt(path +'/Hz_field.csv'.format(nID), unpack=True, delimiter=';')
        # Hz_field1 = Hz_field[::50]
        # DC= np.loadtxt(path +'/DC.csv'.format(nID), unpack=True, delimiter=';')
        # DC1 = DC[::50]
        title = 'M_vs_H{}'.format(mode)
        fig1, ax1 = plt.subplots()
        # ax1.title.set_text(title)
        # c1 = "#D60000"
        # c2 = "#0000FF"

        # color = color_gradient(c1, c2, len(Hz_field1[:,1]))
        
        im1 = ax1.scatter(field_MH65K/10000, magnetic_moment_MH65K, s= 80, facecolors='none', edgecolors='black')
        im1 = ax1.plot(field_MH65K/10000, magnetic_moment_MH65K, lw=2.0, color='red')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Field (Tesla)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Mag_Moment (emu)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.tif')

    if mode == 'MH_100K':
        path = 'G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh'
        # Hz_field= np.loadtxt(path +'/Hz_field.csv'.format(nID), unpack=True, delimiter=';')
        # Hz_field1 = Hz_field[::50]
        # DC= np.loadtxt(path +'/DC.csv'.format(nID), unpack=True, delimiter=';')
        # DC1 = DC[::50]
        title = 'M_vs_H{}'.format(mode)
        fig1, ax1 = plt.subplots()
        # ax1.title.set_text(title)
        # c1 = "#D60000"
        # c2 = "#0000FF"

        # color = color_gradient(c1, c2, len(Hz_field1[:,1]))
        
        im1 = ax1.scatter(field_MH100K/10000, magnetic_moment_MH100K, s= 80, facecolors='none', edgecolors='black')
        im1 = ax1.plot(field_MH100K/10000, magnetic_moment_MH100K, lw=2.0, color='red')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Field (Tesla)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Mag_Moment (emu)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.tif')
        
    if mode == 'MH_150K':
        path = 'G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh'
        # Hz_field= np.loadtxt(path +'/Hz_field.csv'.format(nID), unpack=True, delimiter=';')
        # Hz_field1 = Hz_field[::50]
        # DC= np.loadtxt(path +'/DC.csv'.format(nID), unpack=True, delimiter=';')
        # DC1 = DC[::50]
        title = 'M_vs_H{}'.format(mode)
        fig1, ax1 = plt.subplots()
        # ax1.title.set_text(title)
        # c1 = "#D60000"
        # c2 = "#0000FF"

        # color = color_gradient(c1, c2, len(Hz_field1[:,1]))
        
        im1 = ax1.scatter(field_MH150K/10000, magnetic_moment_MH150K, s= 80, facecolors='none', edgecolors='black')
        im1 = ax1.plot(field_MH150K/10000, magnetic_moment_MH150K, lw=2.0, color='red')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Field (Tesla)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Mag_Moment (emu)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.tif')
        
    if mode == 'MH_200K':
        path = 'G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh'
        # Hz_field= np.loadtxt(path +'/Hz_field.csv'.format(nID), unpack=True, delimiter=';')
        # Hz_field1 = Hz_field[::50]
        # DC= np.loadtxt(path +'/DC.csv'.format(nID), unpack=True, delimiter=';')
        # DC1 = DC[::50]
        title = 'M_vs_H{}'.format(mode)
        fig1, ax1 = plt.subplots()
        # ax1.title.set_text(title)
        # c1 = "#D60000"
        # c2 = "#0000FF"

        # color = color_gradient(c1, c2, len(Hz_field1[:,1]))
        
        im1 = ax1.scatter(field_MH200K/10000, magnetic_moment_MH200K, s= 80, facecolors='none', edgecolors='black')
        im1 = ax1.plot(field_MH200K/10000, magnetic_moment_MH200K, lw=2.0, color='red')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Field (Tesla)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Mag_Moment (emu)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.tif')

    if mode == 'MH_250K':
        path = 'G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh'
        # Hz_field= np.loadtxt(path +'/Hz_field.csv'.format(nID), unpack=True, delimiter=';')
        # Hz_field1 = Hz_field[::50]
        # DC= np.loadtxt(path +'/DC.csv'.format(nID), unpack=True, delimiter=';')
        # DC1 = DC[::50]
        title = 'M_vs_H{}'.format(mode)
        fig1, ax1 = plt.subplots()
        # ax1.title.set_text(title)
        # c1 = "#D60000"
        # c2 = "#0000FF"

        # color = color_gradient(c1, c2, len(Hz_field1[:,1]))
        
        im1 = ax1.scatter(field_MH250K/10000, magnetic_moment_MH250K, s= 80, facecolors='none', edgecolors='black')
        im1 = ax1.plot(field_MH250K/10000, magnetic_moment_MH250K, lw=2.0, color='red')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Field (Tesla)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Mag_Moment (emu)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.tif')
        
    if mode == 'MH_300K':
        path = 'G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh'
        # Hz_field= np.loadtxt(path +'/Hz_field.csv'.format(nID), unpack=True, delimiter=';')
        # Hz_field1 = Hz_field[::50]
        # DC= np.loadtxt(path +'/DC.csv'.format(nID), unpack=True, delimiter=';')
        # DC1 = DC[::50]
        title = 'M_vs_H{}'.format(mode)
        fig1, ax1 = plt.subplots()
        # ax1.title.set_text(title)
        # c1 = "#D60000"
        # c2 = "#0000FF"

        # color = color_gradient(c1, c2, len(Hz_field1[:,1]))
        
        im1 = ax1.scatter(field_MH300K/10000, magnetic_moment_MH300K, s= 80, facecolors='none', edgecolors='black')
        im1 = ax1.plot(field_MH300K/10000, magnetic_moment_MH300K, lw=2.0, color='red')
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Field (Tesla)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Mag_Moment (emu)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.tif')

    if mode == 'multi_MT':
        path = 'G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh'
        # Hz_field= np.loadtxt(path +'/Hz_field.csv'.format(nID), unpack=True, delimiter=';')
        # Hz_field1 = Hz_field[::50]
        # DC= np.loadtxt(path +'/DC.csv'.format(nID), unpack=True, delimiter=';')
        # DC1 = DC[::50]
        title = 'M_vs_H{}'.format(mode)
        fig1, ax1 = plt.subplots()
        # ax1.title.set_text(title)
        # c1 = "#D60000"
        # c2 = "#0000FF"

        # color = color_gradient(c1, c2, len(Hz_field1[:,1]))
        # im1 = ax1.scatter(temperature_MT_ZFC10, magnetic_moment_MT_ZFC10, s= 60, facecolors='none', edgecolors='black')
        # im1 = ax1.plot(temperature_MT_ZFC10, magnetic_moment_MT_ZFC10, lw=2.0, color='red')
        
        # im1 = ax1.scatter(temperature_MT_FC10, magnetic_moment_MT_FC10, s= 60, facecolors='none', edgecolors='black')
        # im1 = ax1.plot(temperature_MT_FC10, magnetic_moment_MT_FC10, lw=2.0, color='red')
        
        im1 = ax1.scatter(temperature_MT_ZFC100, magnetic_moment_MT_ZFC100, s= 60, facecolors='none', edgecolors='black')
        im1 = ax1.plot(temperature_MT_ZFC100, magnetic_moment_MT_ZFC100, lw=2.0, color='red')
        
        im1 = ax1.scatter(temperature_MT_FC100, magnetic_moment_MT_FC100, s= 60, facecolors='none', edgecolors='blue')
        im1 = ax1.plot(temperature_MT_FC100, magnetic_moment_MT_FC100, lw=2.0, color='red')
        
        im1 = ax1.scatter(temperature_MT_FC1000, magnetic_moment_MT_FC1000, s= 60, facecolors='none', edgecolors='green')
        im1 = ax1.plot(temperature_MT_FC1000, magnetic_moment_MT_FC1000, lw=2.0, color='red')
                
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Field (Tesla)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Mag_Moment (emu)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.tif')

    elif mode == 'multi_MH':
        path = 'G:\\My Drive\\Experiments\\Materials\\NiBr2\\21240705_squid_measurements\\7T_squid_CVD_NiBr2_perpen_khagesh'
        # Hz_field= np.loadtxt(path +'/Hz_field.csv'.format(nID), unpack=True, delimiter=';')
        # Hz_field1 = Hz_field[::50]
        # DC= np.loadtxt(path +'/DC.csv'.format(nID), unpack=True, delimiter=';')
        # DC1 = DC[::50]
        title = 'M_vs_H{}'.format(mode)
        fig1, ax1 = plt.subplots()
        # ax1.title.set_text(title)
        # c1 = "#D60000"
        # c2 = "#0000FF"

        # color = color_gradient(c1, c2, len(Hz_field1[:,1]))
        im1 = ax1.scatter(field_MH2K/10000, magnetic_moment_MH2K, s= 80, facecolors='none', edgecolors='#000000')
        im1 = ax1.plot(field_MH2K/10000, magnetic_moment_MH2K, lw=1.0, color='#000000')
        
        im1 = ax1.scatter(field_MH30K/10000, magnetic_moment_MH30K, s= 80, facecolors='none', edgecolors='#191919')
        im1 = ax1.plot(field_MH30K/10000, magnetic_moment_MH30K, lw=1.0, color='#191919')
        
        im1 = ax1.scatter(field_MH45K/10000, magnetic_moment_MH45K, s= 80, facecolors='none', edgecolors='#323232')
        im1 = ax1.plot(field_MH45K/10000, magnetic_moment_MH45K, lw=1.0, color='#323232')
        
        im1 = ax1.scatter(field_MH55K/10000, magnetic_moment_MH55K, s= 80, facecolors='none', edgecolors='#666666')
        im1 = ax1.plot(field_MH55K/10000, magnetic_moment_MH55K, lw=1.0, color='#666666')
        
        # im1 = ax1.scatter(field_MH65K/10000, magnetic_moment_MH65K, s= 80, facecolors='none', edgecolors='#666666')
        # im1 = ax1.plot(field_MH65K/10000, magnetic_moment_MH65K, lw=1.0, color='#666666')
        
        im1 = ax1.scatter(field_MH100K/10000, magnetic_moment_MH100K, s= 80, facecolors='none', edgecolors='#7f7f7f')
        im1 = ax1.plot(field_MH100K/10000, magnetic_moment_MH100K, lw=1.0, color='#7f7f7f')
        
        # im1 = ax1.scatter(field_MH150K/10000, magnetic_moment_MH150K, s= 80, facecolors='none', edgecolors='#999999')
        # im1 = ax1.plot(field_MH150K/10000, magnetic_moment_MH150K, lw=1.0, color='#999999')
        
        im1 = ax1.scatter(field_MH200K/10000, magnetic_moment_MH200K, s= 80, facecolors='none', edgecolors='#999999')
        im1 = ax1.plot(field_MH200K/10000, magnetic_moment_MH200K, lw=1.0, color='#999999')
        
        # im1 = ax1.scatter(field_MH250K/10000, magnetic_moment_MH250K, s= 80, facecolors='none', edgecolors='#cccccc')
        # im1 = ax1.plot(field_MH250K/10000, magnetic_moment_MH250K, lw=1.0, color='#cccccc')
        
        im1 = ax1.scatter(field_MH300K/10000, magnetic_moment_MH300K, s= 80, facecolors='none', edgecolors='#cccccc')
        im1 = ax1.plot(field_MH300K/10000, magnetic_moment_MH300K, lw=1.0, color='#cccccc')
                
        # plt.plot(AC_V[:,1],np.average(li1R[:,1]), color='red')
        ax1.set_xlabel('Field (Tesla)', fontsize=20, family = 'Times New Roman', color='black')  
        ax1.set_ylabel('Mag_Moment (emu)', fontsize=20, family = 'Times New Roman', color='black')
        # ax1.set_xticklabels([])
        # ax1.set_yticklabels([])
        # ax1.set_xticks([])
        # ax1.set_yticks([])
        ax1.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

        fig1.tight_layout()
        # fig1.show()
        fig1.savefig(path + '/' + title + '.tif')
