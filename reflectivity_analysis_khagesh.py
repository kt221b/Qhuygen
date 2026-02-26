import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import correlate, correlation_lags
from tkinter import Tk, filedialog 
import glob
import os

# %%
root = Tk()
root.withdraw()

# Ask user to select a folder
folder = filedialog.askdirectory(title="Select a folder")

# Collect all CSV files in the folder
csv_files = glob.glob(os.path.join(folder, "*.txt"))

data_dict = {}

for f in csv_files:
    filename = os.path.splitext(os.path.basename(f))[0]
    try:
        # Try reading with comma delimiter
        data = np.loadtxt(f, usecols=(0, 1), delimiter=",")
        data_dict[filename] = data
    except Exception as e:
        print(f"Error reading {f}: {e}")

print("Loaded files:", list(data_dict.keys()))
    
# %%
# create calibration
data_calib= np.loadtxt(os.path.dirname(folder)+'/oriel6035_centeredin350nm_test0.TXT', skiprows=75)
data_peaks= np.array([99, 353, 580, 754, 894])
nm_peaks= np.array([253.6, 312.6, 365, 404.7, 435.8])

func = lambda x, a, b: x*a +b
fitresult, _ = curve_fit(func, data_peaks, nm_peaks)
#plt.plot(func(np.arange(1044), *fitresult), data_calib)

center_wls = [300, 400, 500, 600, 700]
NPIXELS = 1024
# import data
bg = np.zeros((len(center_wls), NPIXELS))
z1 = np.zeros((len(center_wls), NPIXELS))
x = np.array([np.arange(NPIXELS)]*len(center_wls), dtype=float)

#amplitudes and shifts corrections eyeballed for now
amplitudes= np.array([1, 1, 1, 1, 1])
shifts= np.array([0, 0, 3.5, 9, 16,])

for i, value in enumerate(center_wls):
    bg[i]= np.loadtxt(folder+'/{:.0f}_sio2_12K.TXT'.format(value), skiprows=75)[10:-10]*amplitudes[i]
    z1[i]= np.loadtxt(folder+'/{:.0f}_fl2_12K.TXT'.format(value), skiprows=75)[10:-10]*amplitudes[i]
    x[i] = func(x[i], fitresult[0], value-119)+shifts[i]

if True:
    plt.figure()
    plt.title('Background')
    for i in range(len(center_wls)):
        plt.plot(x[i], bg[i])
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Normalized Reflectance')

    plt.figure()
    plt.title('Sample')
    for i in range(len(center_wls)):
        plt.plot(x[i], z1[i])
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Normalized Reflectance') 

# %% reflectance plots
plt.figure(1)
plt.title('Reflectance')
for i in range(len(center_wls)):
        plt.plot(x[i], (z1[i])/(bg[i]), c='r')
plt.xlabel('Wavelength (nm)')
#plt.ylim([0.5, 1.9])
plt.ylabel('Normalized Reflectance')

plt.figure(2)
plt.title('Reflectance')
for i in range(len(center_wls)):
        plt.plot(1239.8/x[i], (z1[i])/(bg[i]), c='r')
plt.xlabel('Energy (eV)')
#plt.ylim([0.5, 1.9])
plt.ylabel('Normalized Reflectance')


# %%
