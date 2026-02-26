# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 16:09:28 2025

@author: Principal
"""
import os
import json
import h5py
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib.widgets import PolygonSelector
from matplotlib import path as mplPath
from skimage.draw import polygon2mask
from roipoly import MultiRoi, RoiPoly 
import qcodes as qc
from qcodes import initialise_or_create_database_at, load_by_id
from qcodes.dataset import plot_dataset
from tkinter import Tk, filedialog
#%% Example image
root = Tk()
root.withdraw()  # Hide the root window

db_file_path = filedialog.askopenfilename(title="Select a file")

if db_file_path:
    print("Selected file:", db_file_path)
    root.destroy()
else:
    print("No file selected")
    
qc.initialise_or_create_database_at(db_file_path)
#%%
nID = int(input("Define nID: "))
        
#Define nID in the console as nID = 18
print("ID =", nID)


# qcodes.initialise_or_create_database_at(DB_path_maintenance)
dset = qc.dataset.load_by_id(nID)
data = dset.to_xarray_dataarray_dict()
name = dset.name
experiments = qc.experiments()

#%%
data = qc.load_by_id(nID)

    
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

#%% raw plots (Plots not removing the background)

# DC
redblue = LinearSegmentedColormap.from_list("redblue", ["blue", "white", "red"])

# x = np.linspace(0, 32, 5) # at low temp 150V corresponds to 48.37 micrometer
# y = np.linspace(0, 32, 5)

x = np.linspace(0, 36, 5) # at room temp 60V corresponds to 62.55 micrometer
y = np.linspace(0, 36, 5)

normalized_path = os.path.normpath(db_file_path)
path = os.path.dirname(normalized_path)
path = os.path.join(path, str(nID))
if not os.path.exists(path):
    os.mkdir(path)

fig, ax = plt.subplots(figsize=(5.75, 4.2))
im_dc = ax.imshow(dcX.T, origin='lower', extent=[x[0], x[-1], y[0], y[-1]], cmap='gray', aspect='auto')
cbar_dc = plt.colorbar(im_dc, ax=ax)
cbar_dc.ax.tick_params(labelsize=20, colors='black')
cbar_dc.set_label("mV", fontsize=20, family = 'Arial', color='black')
ax.set_xlabel("\u00B5m", fontsize=20, family = 'Arial', color='black')
ax.set_ylabel("\u00B5m", fontsize=20, family = 'Arial', color='black')
ax.set_title("DC")
ax.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
plt.tight_layout()
plt.show()
fig.savefig(path + '/' + 'ID' + str(nID)+ 'DC' +'.png')


fig, axes = plt.subplots(1, 2, figsize=(11.3, 4.2))
# Kerr
im_Kerr = axes[0].imshow(Kerr.T, origin='lower', extent=[x[0], x[-1], y[0], y[-1]], cmap=redblue, aspect='auto')
cbar_Kerr = plt.colorbar(im_Kerr, ax=axes[0])
cbar_Kerr.set_label("a.u.")
axes[0].set_xlabel("X (V)")
axes[0].set_ylabel("Y (V)")
axes[0].set_title("Kerr")
axes[0].tick_params(labelsize=12)

# RMCD
im_RMCD = axes[1].imshow(RMCD.T, origin='lower', extent=[x[0], x[-1], y[0], y[-1]], cmap=redblue, aspect='auto')
cbar_RMCD = plt.colorbar(im_RMCD, ax=axes[1])
cbar_RMCD.set_label("a.u.")
axes[1].set_xlabel("X (V)")
axes[1].set_ylabel("Y (V)")
axes[1].set_title("RMCD")
axes[1].tick_params(labelsize=12)

plt.tight_layout()
plt.show()

# Helper function for PolygonSelector ROI and mask
class ROISelector:
    def __init__(self, ax, image_shape, x_extent, y_extent):
        self.ax = ax
        self.image_shape = image_shape
        self.x_extent = x_extent
        self.y_extent = y_extent
        self.verts = None
        self.done = False  

        self.selector = PolygonSelector(
            ax, self.onselect,
            props=dict(color='black', linestyle='-', linewidth=2, alpha=0.5),
            handle_props=dict(marker='o', markersize=5, mec='r', mfc='r', alpha=0.5)
        )

        self.cid = plt.connect('button_press_event', self.on_double_click)
        print("Draw ROI polygon with mouse. Double-click to close polygon.")
        plt.show(block=False)   # 🚀 non-blocking

        # event loop until finished
        while not self.done:
            plt.pause(0.1)

    def onselect(self, verts):
        self.verts = verts  

    def on_double_click(self, event):
        if event.dblclick:
            self.verts = self.selector.verts
            self.done = True
            plt.close()

    def get_mask(self):
        if self.done and self.verts is not None:
            arr_verts = []
            for x_disp, y_disp in self.verts:
                col = int(np.round((x_disp - self.x_extent[0]) / (self.x_extent[1] - self.x_extent[0]) * (self.image_shape[1] - 1)))
                row = int(np.round((y_disp - self.y_extent[0]) / (self.y_extent[1] - self.y_extent[0]) * (self.image_shape[0] - 1)))
                arr_verts.append([row, col])
            mask = polygon2mask(self.image_shape, np.array(arr_verts))
            return mask
        else:
            return None

#%% ROI selection and background subtraction for Kerr
print("Draw ROI on substatre for Kerr background subtraction (draw polygon, press enter to finish)")
fig_Kerr, ax_Kerr = plt.subplots(figsize=(5.75, 4.2))
ax_Kerr.imshow(Kerr.T, origin='lower', extent=[x[0], x[-1], y[0], y[-1]], cmap=redblue, aspect='auto')
plt.tight_layout()
plt.title("Kerr select ROI on susbtrate")
roi_Kerr = ROISelector(ax_Kerr, Kerr.shape, [x[0], x[-1]], [y[0], y[-1]])
mask_Kerr = roi_Kerr.get_mask()
if mask_Kerr is not None:
    substrate_average_k = Kerr[mask_Kerr].mean()
    Kerr_bc = Kerr - substrate_average_k
    print(f"Kerr substrate average: {substrate_average_k}")
else:
    print("No ROI selected for Kerr!")
    Kerr_bc = Kerr
#%% Show background-corrected Kerr
fig, ax = plt.subplots(figsize=(5.75, 4.2))
im_Kerr = ax.imshow(Kerr_bc.T, origin='lower', extent=[x[0], x[-1], y[0], y[-1]], cmap=redblue, aspect='auto', vmin=-0.03, vmax=0.03)
cbar_Kerr = plt.colorbar(im_Kerr, ax=ax)
cbar_Kerr.ax.tick_params(labelsize=20, colors='black')
cbar_Kerr.set_label("Kerr (a.u.)", fontsize=20, family = 'Arial', color='black')
ax.set_xlabel("\u00B5m", fontsize=20, family = 'Arial', color='black') 
ax.set_ylabel("\u00B5m", fontsize=20, family = 'Arial', color='black') 
ax.set_title("Kerr (background corrected)")
ax.set_xlim(x[0], x[-1])
ax.set_ylim(y[0], y[-1])
ax.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
plt.tight_layout()
plt.show()
fig.savefig(path + '/' + 'ID' + str(nID)+ 'Kerr' +'.png')
print("Kerr.png saved!")

#%% Average of the flake after subtraction
# Select ROI for Kerr flake subtraction (draw polygon, double-click to close)
print("Draw ROI on flke to get mean Kerr from flake (draw polygon, double-click to close)")
fig_Kerr_flake, ax_Kerr_flake = plt.subplots(figsize=(5.75, 4.2))
ax_Kerr_flake.imshow(Kerr_bc, origin='lower', extent=[x[0], x[-1], y[0], y[-1]], cmap=redblue, aspect='auto', vmin=-0.05, vmax=0.05)
plt.tight_layout()
plt.title("Kerr select ROI on flake")
roi_Kerr_flake = ROISelector(ax_Kerr_flake, Kerr_bc.shape, [x[0], x[-1]], [y[0], y[-1]])

# Calculate the mean Kerr from the ROI of the flake
mask_Kerr_flake = roi_Kerr_flake.get_mask()
if mask_Kerr_flake is not None:
    flake_average_Kerr = Kerr_bc[mask_Kerr_flake].mean()
    print(f"Kerr flake average: {flake_average_Kerr}")
else:
    print("No ROI selected for Kerr!")
    Kerr_bc = Kerr

#%% ROI selection and background subtraction for RMCD


#**********************RMCD Corrections******************

#%% ROI selection and background subtraction for RMCD
print("Draw ROI on substatre for RMCD background subtraction (draw polygon, press enter to finish)")
fig_RMCD, ax_RMCD = plt.subplots(figsize=(5.75, 4.2))
ax_RMCD.imshow(RMCD.T, origin='lower', extent=[x[0], x[-1], y[0], y[-1]], cmap=redblue, aspect='auto')
plt.tight_layout()
plt.title("RMCD select ROI on susbtrate")
roi_RMCD = ROISelector(ax_RMCD, RMCD.shape, [x[0], x[-1]], [y[0], y[-1]])
mask_RMCD = roi_RMCD.get_mask()
if mask_RMCD is not None:
    substrate_average_r = RMCD[mask_RMCD].mean()
    RMCD_bc = RMCD - substrate_average_r
    print(f"RMCD substrate average: {substrate_average_r}")
else:
    print("No ROI selected for RMCD!")
    RMCD_bc = RMCD

#%% Show background-corrected RMCD
fig, ax = plt.subplots(figsize=(5.75, 4.2))
im = ax.imshow(RMCD_bc.T, origin='lower', extent=[x[0], x[-1], y[0], y[-1]], cmap=redblue, aspect='auto', vmin=-0.03, vmax=0.03)
cbar_RMCD = plt.colorbar(im, ax=ax)
cbar_RMCD.ax.tick_params(labelsize=20, colors='black')
cbar_RMCD.set_label("RMCD (a.u.)", fontsize=20, family = 'Arial', color='black') 
ax.set_xlabel("\u00B5m", fontsize=20, family = 'Arial', color='black')
ax.set_ylabel("\u00B5m", fontsize=20, family = 'Arial', color='black')
ax.set_title("RMCD (background corrected)")
ax.set_xlim(x[0], x[-1])
ax.set_ylim(y[0], y[-1])
ax.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
plt.tight_layout()
plt.show()
fig.savefig(path + '/' + 'ID' + str(nID)+ 'RMCD' +'.png')
print("RMCD.png saved!")

#%% Average of the flake after subtraction
# Select ROI for RMCD flake subtraction (draw polygon, double-click to close)
print("Draw ROI on flke to get mean RMCD from flake (draw polygon, double-click to close)")
fig_RMCD_flake, ax_RMCD_flake = plt.subplots(figsize=(5.75, 4.2))
ax_RMCD_flake.imshow(RMCD_bc, origin='lower', extent=[x[0], x[-1], y[0], y[-1]], cmap=redblue, aspect='auto', vmin=-0.05, vmax=0.05)
plt.tight_layout()
plt.title("RMCD select ROI on flake")
roi_RMCD_flake = ROISelector(ax_RMCD_flake, RMCD_bc.shape, [x[0], x[-1]], [y[0], y[-1]])

# Calculate the mean RMCD from the ROI of the flake
mask_RMCD_flake = roi_RMCD_flake.get_mask()
if mask_RMCD_flake is not None:
    flake_average_RMCD = RMCD_bc[mask_RMCD_flake].mean()
    print(f"RMCD flake average: {flake_average_RMCD}")
else:
    print("No ROI selected for RMCD!")
    RMCD_bc = RMCD
    
#%%# =========================
# Save results to Excel
# =========================
# results_file = "results.csv"   # change path if you want it somewhere fixed
parent_path = os.path.dirname(path)
results_file = os.path.join(parent_path, "results1.csv")
field= name.split("_")[-1]
# Collect results in a dict
results_dict = {
    "field":[field],
    "nID": [nID],
    "Kerr_flake_avg": [flake_average_Kerr if mask_Kerr_flake is not None else None],
    "RMCD_flake_avg": [flake_average_RMCD if mask_RMCD_flake is not None else None]
}

df_new = pd.DataFrame(results_dict)

# Append if file exists, otherwise create new
if os.path.exists(results_file):
    df_existing = pd.read_csv(results_file)
    df_all = pd.concat([df_existing, df_new], ignore_index=True)
else:
    df_all = df_new

# Write back to CSV
df_all.to_csv(results_file, index=False)

print(f"✅ Results for ID {nID} saved to {results_file}")
