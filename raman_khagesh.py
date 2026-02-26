# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
# import matplotlib.colors as mcolors
from matplotlib import colormaps
from tkinter import Tk, filedialog 
from scipy.ndimage import label
import glob
import os

# x1, y1 = np.loadtxt(r'G:\My Drive\Experiments\Materials\CrTe2\CVT_acitonitrile_iodine_3rd_try\Raman\Red_mW_250micro_0ND_site1_20sec.txt', skiprows=3, delimiter=';',usecols =(0, 1), unpack = True)
# %%
root = Tk()
root.withdraw()

# Open file dialog to select a file
file_path = filedialog.askopenfilename(
    title="Select a file",
    filetypes=[("Data files", "*.txt *.dat *.csv"), ("All files", "*.*")]
)

folder = os.path.dirname(file_path)

txt_files = glob.glob(os.path.join(folder, "*.txt"))

data_dict = {}

for f in txt_files:
    filename = os.path.splitext(os.path.basename(f))[0]
    try:
        try:
            data = np.loadtxt(f, usecols=(0, 1), delimiter=";")
        except:
            data = np.loadtxt(f, usecols=(0, 1))
        data_dict[filename] = data
    except Exception as e:
        print(f"Error reading {f}: {e}")
    
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
    data = np.loadtxt(file_path, usecols=(0, 1),delimiter=';', skiprows=3)
except:
    pass

try:
    data = np.loadtxt(file_path, usecols=(0, 1),delimiter='\t', skiprows=3)
except:
    pass
    
# %%
fig, ax = plt.subplots(layout='constrained')
# ax.set_ylim(0, 1)
# ax.set_xlim(50, 200)

# num_files = len(data_dict)
# colors = colormaps["plasma"](np.linspace(0, 1, num_files))

# for i, (filename, data) in enumerate(data_dict.items()):
#     ax.plot(data[:, 0], data[:, 1]/1000, label=filename, color=colors[i])
# data = data_dict[list(data_dict.keys())[9]]

x = data[:, 0]
y = data[:, 1]

# # Compute mean and std on y
# mean = np.mean(y)
# std = np.std(y)

# # Boolean mask for filtering spikes
# mask = np.abs(y - mean) < 3*std

# # Apply mask to both x and y
# x_filtered = x[mask]
# y_filtered = y[mask]

ax.plot(x, y/1000, color='black')

ax.set_ylabel('Intensity (a.u.) x$10^{3}$', fontsize=22, family = 'Arial', color='black')
ax.set_xlabel('Raman Shift (cm$^{-1}$)', fontsize=22, family = 'Arial', color='black')

# ax.set_xticklabels(np.arange(0,225,25), fontsize=12, family = 'Times New Roman')
# ax.set_yticklabels(np.arange(600, 1500, 100), fontsize=22, family = 'Times New Roman')
# ax.legend([x1,y1], ["B","C"])
ax.set_title("All .txt Files in Folder")
# ax.legend(loc='best')

ax.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
# fig.savefig(r'G:\My Drive\Experiments\Materials\CrTe2\CVT_acitonitrile_iodine_3rd_try\Raman\Red_mW_250micro_0ND_site1_20sec.tif')
fig.savefig(file_path + '.png')

# %%
fig, ax = plt.subplots(layout='constrained')
# ax.set_ylim(0, 1)
ax.set_xlim(50, 700)

x = data[:, 0]
y = data[:, 1]

# --- Adaptive spike removal (width-based) ---
# Smooth baseline with moving average to capture general trend
window = 101  # bigger window -> smoother baseline
y_baseline = np.convolve(y, np.ones(window)/window, mode='same')

# Deviation from baseline
deviation = y - y_baseline

# Threshold for detecting spikes
thr = 2 * np.std(deviation)   # lower factor = more aggressive
spike_mask = deviation > thr

# Label contiguous spike regions
labels, num = label(spike_mask)

# Minimum width (in points) to keep as real peak
min_width = 5   # increase to remove spikes like at 450 & 620

# Build final mask
mask = np.ones_like(y, dtype=bool)
for lab in range(1, num + 1):
    idx = np.where(labels == lab)[0]
    if len(idx) < min_width:   # narrow spike -> remove
        mask[idx] = False

# Filtered data
x_filtered = x[mask]
y_filtered = y[mask]


ax.plot(x_filtered, y_filtered/1000, label='filtered', color='black')

ax.set_ylabel('Intensity (a.u.) x$10^{3}$', fontsize=22, family = 'Arial', color='black')
ax.set_xlabel('Raman Shift (cm$^{-1}$)', fontsize=22, family = 'Arial', color='black')

# ax.set_xticklabels(np.arange(0,225,25), fontsize=12, family = 'Times New Roman')
# ax.set_yticklabels(np.arange(600, 1500, 100), fontsize=22, family = 'Times New Roman')
# ax.legend([x1,y1], ["B","C"])
ax.set_title("All .txt Files in Folder")
# ax.legend(loc='best')

ax.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')

# fig.savefig(r'G:\My Drive\Experiments\Materials\CrTe2\CVT_acitonitrile_iodine_3rd_try\Raman\Red_mW_250micro_0ND_site1_20sec.tif')
fig.savefig(file_path + '.png')