# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 12:04:44 2026

@author: Principal
"""

import numpy as np
import matplotlib.pyplot as plt

def solve_nibr2_inplane(Bx, Bz, J1, J3, J_ex, D=0.15):
    # Constants
    g_ni = 2.21      # Updated for NiBr2
    mu_B = 0.05788   # meV/T
    
    # 1. Operators
    Sz = np.diag([1, 0, -1])
    Sp = np.array([[0, np.sqrt(2), 0], [0, 0, np.sqrt(2)], [0, 0, 0]])
    Sm = Sp.conj().T
    Sx, Sy = (Sp + Sm) / 2, (Sp - Sm) / 2j
    I3, I2 = np.eye(3), np.eye(2)
    sz, sx, sy = 0.5*np.array([[1,0],[0,-1]]), 0.5*np.array([[0,1],[1,0]]), 0.5*np.array([[0,-1j],[1j,0]])

    # 2. 18D Operators
    S1z, S1x, S1y = np.kron(Sz, np.kron(I3, I2)), np.kron(Sx, np.kron(I3, I2)), np.kron(Sy, np.kron(I3, I2))
    S2z, S2x, S2y = np.kron(I3, np.kron(Sz, I2)), np.kron(I3, np.kron(Sx, I2)), np.kron(I3, np.kron(Sy, I2))
    sig_z, sig_x, sig_y = 2*np.kron(I3, np.kron(I3, sz)), 2*np.kron(I3, np.kron(I3, sx)), 2*np.kron(I3, np.kron(I3, sy))

    # 3. Hamiltonian Components
    H_zeeman = g_ni * mu_B * (Bx * (S1x + S2x) + Bz * (S1z + S2z))
    H_anisotropy = D * (S1z**2 + S2z**2)
    
    # Lattice Exchange: J1 and J3 competition
    # In a 2-site approximation, the "Total Exchange" J_eff = J1 + J3 
    # (assuming the sites are effectively neighbors in the helical path)
    H_lattice = (J1 + J3) * (S1x @ S2x + S1y @ S2y + S1z @ S2z)
    
    H_tunnel = J_ex * (S1x @ sig_x + S1y @ sig_y + S1z @ sig_z)

    return np.linalg.eigvalsh(H_zeeman + H_anisotropy + H_lattice + H_tunnel)

#%%
T_kelvin = 10      # Temperature of your cryostat
kb = 0.08617        # meV/K
beta = 1.0 / (kb * T_kelvin)

Bx_fields = np.linspace(-7, 7, 50)  # 50 points
avg_energies = []

for B in Bx_fields:
    # 1. Get all 18 eigenvalues for this field
    energies = solve_nibr2_inplane(B, 0, -1.5, 0.41, 0.2, 0.5)
    
    # 2. Shift to avoid numerical overflow (relative to ground state)
    E_min = np.min(energies)
    shifted_E = energies - E_min
    
    # 3. Calculate Boltzmann Weights: P_i = exp(-E_i / kT) / Z
    weights = np.exp(-beta * shifted_E)
    Z = np.sum(weights)
    
    # 4. Thermal Average of the Excitation Energy
    avg_E = np.sum(shifted_E * weights) / Z
    avg_energies.append(avg_E)

# Convert to numpy array to ensure shapes match
avg_energies = np.array(avg_energies)

# --- Plotting ---
plt.figure(figsize=(9, 5))
plt.plot(Bx_fields, avg_energies, color='purple', linewidth=2, label=f'Avg State at {T_kelvin}K')
plt.title("Statistical Average Energy of the NiBr2 Barrier")
plt.xlabel("In-Plane Magnetic Field $B_x$ (Tesla)")
plt.ylabel("Average Excitation Energy $\\langle E \\rangle$ (meV)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()