# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 13:17:39 2026

@author: Principal
"""

import numpy as np
import matplotlib.pyplot as plt


def PEM(delta):
    """Jones Matrix for a PEM (fast axis at 0 degrees)."""
    return np.array([[np.exp(1j * delta / 2), 0],
                     [0, np.exp(-1j * delta / 2)]])

def polarizer(theta_deg):
    """Standard Jones Matrix for a Linear Polarizer at angle theta."""
    theta = np.deg2rad(theta_deg)
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c**2, c*s],
                     [c*s, s**2]])
# Parameters
t = np.linspace(0, 2*np.pi, 500) 
amplitudes = [np.pi/4, np.pi/2, np.pi] 
# labels = ['$\pi/4$ (Low)', '$\pi/2$ ($\lambda/4$ Peak)', '$\pi$ ($\lambda/2$ Peak)']

# Initial Light: Linear Horizontal (1, 0)
# E_in = polarizer(45) @ np.array([1, 0])
E_in = (1/np.sqrt(2)) * np.array([1, 1])
# Analyzer at 45 degrees to see the interference/retardation
# This is where the 'magic' happens for the plot!
# J_analyzer = analyzer_matrix(np.deg2rad(45))
# 2. Create the "There and Back" Retardation Path
# Sweep from 0 to pi (lambda/2) and back to 0
up = np.linspace(0, np.pi, 5)
down = np.linspace(np.pi, 0, 5)[1:] # Avoid repeating the pi snapshot
deltas = np.concatenate([up, down])

# Labels to help track the transition
labels = ['0', '$\pi/4$', '$\pi/2$ (L/4)', '$3\pi/4$', '$\pi$ (L/2)', 
           '$3\pi/4$', '$\pi/2$ (L/4)', '$\pi/4$', '0']

fig, axes = plt.subplots(1, len(deltas), figsize=(22, 3))
tau = np.linspace(0, 2*np.pi, 100) # Fast light wave oscillation

for i, d in enumerate(deltas):
    # Calculate state after PEM
    E_out = PEM(d) @ E_in
    
    # Trace the E-field vector over one optical period
    Ex = np.real(E_out[0] * np.exp(1j * tau))
    Ey = np.real(E_out[1] * np.exp(1j * tau))
    
    axes[i].plot(Ex, Ey, 'darkblue', lw=2)
    axes[i].set_title(f"$\delta$ = {labels[i]}")
    axes[i].set_xlim(-1, 1); axes[i].set_ylim(-1, 1)
    axes[i].set_aspect('equal')
    axes[i].axhline(0, color='black', lw=0.5); axes[i].axvline(0, color='black', lw=0.5)
    axes[i].axis('off') # Clean look

plt.suptitle("PEM $\lambda/2$ Cycle: Linear (45°) -> Circular -> Linear (-45°) -> Circular -> Linear (45°)", fontsize=14)
plt.show()


#%%

# 1. Setup Input: Normalized 45° Light
E_in = (1/np.sqrt(2)) * np.array([1, 1])

# 2. Create the "There and Back" Retardation Path for Quarter-Wave
# Sweep from 0 to pi/2 (lambda/4) and back to 0
up = np.linspace(0, np.pi/2, 5)
down = np.linspace(np.pi/2, 0, 5)[1:] # Avoid repeating the peak
deltas = np.concatenate([up, down])

# Labels for the specific retardation values
labels = ['0 (Lin)', '$\pi/8$', '$\pi/4$', '$3\pi/8$', '$\pi/2$ (Circ)', 
          '$3\pi/8$', '$\pi/4$', '$\pi/8$', '0 (Lin)']

fig, axes = plt.subplots(1, len(deltas), figsize=(20, 3))
tau = np.linspace(0, 2*np.pi, 100) # Fast light wave oscillation

for i, d in enumerate(deltas):
    # Calculate Jones Vector after PEM
    E_out = PEM(d) @ E_in
    
    # Trace the E-field vector path (Lissajous curve)
    Ex = np.real(E_out[0] * np.exp(1j * tau))
    Ey = np.real(E_out[1] * np.exp(1j * tau))
    
    axes[i].plot(Ex, Ey, 'teal', lw=2)
    axes[i].set_title(f"$\delta$ = {labels[i]}")
    axes[i].set_xlim(-1, 1); axes[i].set_ylim(-1, 1)
    axes[i].set_aspect('equal')
    axes[i].axhline(0, color='black', lw=0.5); axes[i].axvline(0, color='black', lw=0.5)
    axes[i].axis('off')

plt.suptitle("PEM $\lambda/4$ Cycle: Linear (45°) $\leftrightarrow$ Circular", fontsize=14)
plt.show()

#%%
#intensities
t = np.linspace(0, 2*np.pi, 500) 
amplitudes = [np.pi/4, np.pi/2, np.pi] 
labels = ['$\pi/4$ (Low)', '$\pi/2$ ($\lambda/4$ Peak)', '$\pi$ ($\lambda/2$ Peak)']

# Initial Light: Polarized at 45 degrees
# E_in = polarizer(45) @ np.array([1, 0])
E_in = (1/np.sqrt(2)) * np.array([1, 1])

plt.figure(figsize=(10, 6))

for amp, label in zip(amplitudes, labels):
    delta_t = amp * np.sin(t)
    intensities = []
    
    for d in delta_t:
        # CORRECTED SYSTEM: E_in -> PEM -> Analyzer
        # Multiply right to left: Analyzer @ PEM @ E_in
        E_out = polarizer(-45)@PEM(d) @ E_in
        
        # Calculate Intensity
        intensity = np.sum(np.abs(E_out)**2)
        intensities.append(intensity)
    
    plt.plot(t, intensities, label=f'Peak Retardation: {label}')

plt.title('Visible PEM Intensity Oscillations (Corrected Matrix Order)')
plt.xlabel('Time (One Cycle $\omega t$)')
plt.ylabel('Detected Intensity (A.U.)')
plt.xticks([0, np.pi/2, np.pi, 1.5*np.pi, 2*np.pi], ['0', '$\pi/2$', '$\pi$', '$3\pi/2$', '$2\pi$'])
# plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.show()
