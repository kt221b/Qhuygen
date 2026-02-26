# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 09:35:53 2025

@author: Principal
"""

import numpy as np
import matplotlib.pyplot as plt

# Define parameters
omega_t_vals = np.linspace(0, 2 * np.pi, 12)  # omega * t values
delta_0 = np.pi  # peak retardance = pi (half-wave)

# Input Jones vector for 45° linear polarization
E_in = np.array([1, 1]) / np.sqrt(2)

# Lists to store results
ellipticity = []
orientation = []

# Function to compute orientation and ellipticity from Jones vector
def jones_to_ellipse_params(E):
    Ex, Ey = E
    delta_phi = np.angle(Ey) - np.angle(Ex)
    a = np.abs(Ex)
    b = np.abs(Ey)

    # Ellipticity angle (chi): relates to circularity
    chi = 0.5 * np.arcsin(np.sin(delta_phi) * b / np.sqrt(a*2 + b*2))

    # Orientation angle (psi): major axis orientation of the ellipse
    psi = 0.5 * np.arctan2(2 * a * b * np.cos(delta_phi), a*2 - b*2)

    return np.rad2deg(psi), np.rad2deg(chi)

# Compute parameters for each omega * t
for ot in omega_t_vals:
    delta = delta_0 * np.sin(ot)  # time-dependent retardation
    E_out = np.array([1, np.exp(1j * delta)]) / np.sqrt(2)  # output Jones vector
    psi, chi = jones_to_ellipse_params(E_out)
    orientation.append(psi)
    ellipticity.append(chi)

# Plot results
fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

ax[0].plot(np.rad2deg(omega_t_vals), orientation, marker='o')
ax[0].set_ylabel("Orientation Angle ψ (degrees)")
ax[0].set_title("Polarization Ellipse Orientation vs ωt")
ax[0].grid(True)

ax[1].plot(np.rad2deg(omega_t_vals), ellipticity, marker='o', color='orange')
ax[1].set_ylabel("Ellipticity Angle χ (degrees)")
ax[1].set_xlabel("ωt (degrees)")
ax[1].set_title("Ellipticity (Shape of Polarization) vs ωt")
ax[1].grid(True)

plt.tight_layout()
plt.show()