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
#%%    
qc.initialise_or_create_database_at(db_file_path)

if 'db_file_path' in globals() and db_file_path:
    qc.initialise_or_create_database_at(db_file_path)
    print("Database refreshed:", db_file_path)
else:
    print("db_file_path is not defined")
#%%
nID = int(input("Define nID: "))
        
#Define nID in the console as nID = 18
print("ID =", nID)


# qcodes.initialise_or_create_databas242e24_at(DB_path_maintenance)
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
    dcX = data.get_parameter_data('DCli_tr1_data')['DCli_tr1_data']['DCli_tr1_data']
    f1X = data.get_parameter_data('f1li_ch1_databuffer')['f1li_ch1_databuffer']['f1li_ch1_databuffer']
    f2X = data.get_parameter_data('f2li_ch1_databuffer')['f2li_ch1_databuffer']['f2li_ch1_databuffer']
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
    dcX=dcX.reshape(101, 101)
    f1X=f1X.reshape(101, 101)
    f2X=f2X.reshape(101, 101)
    # dcX = dcX.reshape(len(dcX), len(dcX))
    # f1X = f1X.reshape(len(f1X), len(f1X))
    # f2X = f2X.reshape(len(f2X), len(f2X))
except:
    pass
    
RMCD = f1X/dcX
Kerr = f2X/dcX
WC=f2X/(dcX+f1X) #Wollaston contrast
#%% raw plots (Plots not removing the background)

# DC
redblue = LinearSegmentedColormap.from_list("redblue", ["blue", "white", "red"])

x = np.linspace(0, 35, 4) #for LT 150V is 48.3 um, for Room T 60 is 62.5 um
y = np.linspace(0, 35, 4)

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
            props=dict(color='r', linestyle='-', linewidth=2, alpha=0.5),
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
print("Draw ROI for Kerr background subtraction (draw polygon, press enter to finish)")
fig_Kerr, ax_Kerr = plt.subplots(figsize=(5.75, 4.2))
ax_Kerr.imshow(Kerr.T, origin='lower', extent=[x[0], x[-1], y[0], y[-1]], cmap=redblue, aspect='auto')
plt.tight_layout()
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
im_Kerr = ax.imshow(Kerr_bc.T, origin='lower', extent=[x[0], x[-1], y[0], y[-1]], cmap=redblue, aspect='auto', vmin=-0.1, vmax=0.1)
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
#%% ROI selection and background subtraction for RMCD
print("Draw ROI for RMCD background subtraction (draw polygon, press enter to finish)")
fig_RMCD, ax_RMCD = plt.subplots(figsize=(5.75, 4.2))
ax_RMCD.imshow(RMCD.T, origin='lower', extent=[x[0], x[-1], y[0], y[-1]], cmap=redblue, aspect='auto')
plt.tight_layout()
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
im = ax.imshow(RMCD_bc.T, origin='lower', extent=[x[0], x[-1], y[0], y[-1]], cmap=redblue, aspect='auto', vmin=-0.1, vmax=0.1)
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

#%% ROI selection and background subtraction for Wollaston contrast
print("Draw ROI for WC background subtraction (draw polygon, press enter to finish)")
fig_WC, ax_WC = plt.subplots(figsize=(5.75, 4.2))
ax_WC.imshow(WC.T, origin='lower', extent=[x[0], x[-1], y[0], y[-1]], cmap=redblue, aspect='auto')
plt.tight_layout()
roi_WC = ROISelector(ax_WC, WC.shape, [x[0], x[-1]], [y[0], y[-1]])
mask_WC = roi_WC.get_mask()
if mask_WC is not None:
    substrate_average_WC = WC[mask_WC].mean()
    WC_bc = WC - substrate_average_WC
    print(f"WC substrate average: {substrate_average_WC}")
else:
    print("No ROI selected for WC!")
    WC_bc = WC
#%% Show background-corrected Kerr
fig, ax = plt.subplots(figsize=(5.75, 4.2))
im_WC = ax.imshow(WC_bc.T, origin='lower', extent=[x[0], x[-1], y[0], y[-1]], cmap=redblue, aspect='auto', vmin=-0.1, vmax=0.1)
cbar_WC = plt.colorbar(im_WC, ax=ax)
cbar_WC.ax.tick_params(labelsize=20, colors='black')
cbar_WC.set_label("Wollaston Contrast (a.u.)", fontsize=20, family = 'Arial', color='black')
ax.set_xlabel("\u00B5m", fontsize=20, family = 'Arial', color='black') 
ax.set_ylabel("\u00B5m", fontsize=20, family = 'Arial', color='black') 
ax.set_title("Wollastob contrast (background corrected)")
ax.set_xlim(x[0], x[-1])
ax.set_ylim(y[0], y[-1])
ax.tick_params(axis='both', labelsize= 'xx-large', length=10, which='major')
plt.tight_layout()
plt.show()
fig.savefig(path + '/' + 'ID' + str(nID)+ 'WC' +'.png')
print("WC.png saved!")