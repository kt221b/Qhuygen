# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 14:08:16 2025

@author: Principal
"""

import numpy as np
import matplotlib.pyplot as plt

# === Load atomic coordinates ===
import numpy as np

# Read file manually, ignoring lines with too few columns
coords_list = []
with open("atoms-coords.data", "r") as f:
    for line in f:
        if line.strip().startswith("#"):  # skip comments
            continue
        parts = line.split()
        if len(parts) >= 5:  # expected format: index type x y z
            coords_list.append([float(parts[2]), float(parts[3]), float(parts[4])])

coords = np.array(coords_list)
print("First 5 coordinates:\n", coords[:5])


# === Load spins ===
# Format: Sx Sy Sz
spins = np.loadtxt("spins-00000000.data", usecols=(0, 1, 2), skiprows=1)


# Ensure both have the same length
n_atoms = min(coords.shape[0], spins.shape[0])
coords = coords[:n_atoms]
spins = spins[:n_atoms]

# === 3D quiver plot ===
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

ax.quiver(
    coords[:, 0], coords[:, 1], coords[:, 2],  # atom positions
    spins[:, 0], spins[:, 1], spins[:, 2],    # spin vectors
    length=0.5, normalize=True, color="blue"
)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Spin Configuration from Vampire")

plt.show()

