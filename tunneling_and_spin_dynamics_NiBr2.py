# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 12:04:44 2026

@author: Principal
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import sparse
from scipy.sparse.linalg import eigsh

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
#%%

def calculate_transmission(E, V0, d, m_eff=1.0):
    """
    Calculates the transmission probability T(E) for a rectangular barrier.
    E: Electron energy (meV)
    V0: Barrier height (meV)
    d: Barrier thickness (Angstroms)
    m_eff: Effective mass (relative to electron mass m0)
    """
    # Physical Constants
    hbar = 6.5821e-13  # meV * s
    m0 = 5.6856e-32    # meV * s^2 / Angstrom^2 (mass of electron in these units)
    m = m_eff * m0
    
    # Avoid division by zero at E=0 or E=V0
    E = np.where(E == 0, 1e-9, E)
    E = np.where(E == V0, V0 - 1e-9, E)
    
    if np.all(E < V0):
        # Case 1: E < V0 (Tunneling / evanescent waves)
        alpha = np.sqrt(2 * m * (V0 - E)) / hbar
        term = (V0**2) / (4 * E * (V0 - E))
        T = 1 / (1 + term * (np.sinh(alpha * d))**2)
    else:
        # Case 2: E > V0 (Over-barrier transmission)
        # Using the sin version as per the PDF Eq 1.29
        k_prime = np.sqrt(2 * m * (E - V0)) / hbar
        term = (V0**2) / (4 * E * (E - V0))
        T = 1 / (1 + term * (np.sin(k_prime * d))**2)
        
    return T

# --- Setup Parameters ---
thickness = 6.20  # 10 Angstroms
barrier_height = 500.0  # 500 meV
energies = np.linspace(1, 1000, 500) # Sweep energy from 1 to 1000 meV

# Calculate T
T_values = calculate_transmission(energies, barrier_height, thickness)

# --- Plotting ---
plt.figure(figsize=(8, 5))
plt.plot(energies, T_values, label=f'd = {thickness} Å, $V_0$ = {barrier_height} meV', color='blue')
plt.axvline(barrier_height, color='red', linestyle='--', label='Barrier Height $V_0$')
plt.title("Non-Magnetic Tunneling Probability $T(E)$")
plt.xlabel("Electron Energy $E$ (meV)")
plt.ylabel("Transmission Probability $T$")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

#%%

def solve_monolayer_conductance():
    # --- Physical Constants ---
    hbar = 6.5821e-13  # meV * s
    m0 = 5.6856e-32    # mass of electron (meV * s^2 / A^2)
    
    # --- Device Parameters ---
    d = 10.0           # Thickness (Angstroms) [cite: 235]
    E_f = 250.0        # Fermi energy of leads (meV) [cite: 236]
    V0 = 500.0         # Average Barrier Height (meV) [cite: 182]
    
    # --- Magnetic Parameters ---
    # Dimensionless field H = B / B_sat
    H_sweep = np.linspace(-1.5, 1.5, 300) 
    
    # For a monolayer, the angle phi follows the field linearly until saturation
    # cos(phi) = H for |H| <= 1, else sgn(H) [cite: 145]
    cos_phi = np.clip(H_sweep, -1, 1) 
    
    # --- Transmission Probability T(E) ---
    # Using the formula for E < V0 
    alpha = np.sqrt(2 * m0 * (V0 - E_f)) / hbar
    prefactor = (V0**2) / (4 * E_f * (V0 - E_f))
    T_base = 1 / (1 + prefactor * (np.sinh(alpha * d))**2)
    
    # --- Conductance G(H) ---
    # We use the linear model from the PDF 
    # C1 and C2 represent the spin-independent and dependent parts
    C1, C2 = 0.8, 0.2  
    G_normalized = C1 + C2 * cos_phi
    
    # Multiply by T_base to get the 'Real' Conductance scale
    G_total = T_base * G_normalized

    # --- Plotting ---
    plt.figure(figsize=(8, 5))
    plt.plot(H_sweep, G_total, color='darkred', lw=2)
    plt.axhline(T_base * (C1 + C2), color='gray', ls='--', label='Saturation (FM)')
    plt.axhline(T_base * (C1 - C2), color='gray', ls=':', label='Opposite Alignment')
    plt.title("Monolayer Vertical Device: Conductance $G$ vs $H$")
    plt.xlabel("Magnetic Field $H$ (Dimensionless)")
    plt.ylabel("Conductance (Arbitrary Units)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()

solve_monolayer_conductance()
#%%
# Re-using the transmission function from Step 1
def calculate_transmission(E, V0, d, m_eff=1.0):
    hbar = 6.5821e-13  # meV * s
    m0 = 5.6856e-32    # meV * s^2 / A^2
    m = m_eff * m0
    
    # Case: Tunneling (E < V0)
    alpha = np.sqrt(2 * m * (V0 - E)) / hbar
    term = (V0**2) / (4 * E * (V0 - E))
    return 1 / (1 + term * (np.sinh(alpha * d))**2)

def simulate_magnetic_conductance():
    # 1. Parameters from the PDF (Section 1.5)
    d = 10.0           # Thickness (A)
    E_fermi = 250.0    # Electron energy (meV)
    V_P = 450.0        # Barrier for Parallel spins (meV)
    V_AP = 550.0       # Barrier for Anti-Parallel spins (meV)
    
    # Fitting constants from Wang et al. (Bilayer case)
    C1 = 0.810         # [cite: 242]
    C2 = 0.188         # [cite: 242]
    
    # 2. Magnetic Field Sweep (Dimensionless H = B / B_saturation)
    # H ranges from -2 to 2 as in Fig 1.7 of the PDF
    H_sweep = np.linspace(-2, 2, 500)
    
    # 3. Calculate relative angle theta_H for a Bilayer
    # According to Eq 1.32: theta_H = cos(2 * arccos(H))
    # We clip H between -1 and 1 for the arccos calculation
    H_clipped = np.clip(H_sweep, -1, 1)
    theta_H = np.cos(2 * np.arccos(H_clipped)) # [cite: 241]
    
    # 4. Calculate Normalized Conductance G/G0
    # G/G0 = C1 + C2 * cos(theta_H) [cite: 239]
    G_normalized = C1 + C2 * theta_H
    
    # Optional: Calculate absolute G_P and G_AP based on transmission
    T_P = calculate_transmission(E_fermi, V_P, d)
    T_AP = calculate_transmission(E_fermi, V_AP, d)
    
    # --- Plotting ---
    plt.figure(figsize=(9, 5))
    plt.plot(H_sweep, G_normalized, label='Bilayer Conductance (Wang Model)', color='darkblue', linewidth=2)
    plt.title("Tunneling Conductance $G(H)$ for a Bilayer Monolayer")
    plt.xlabel("Dimensionless Magnetic Field $H$")
    plt.ylabel("Normalized Conductance $G/G_0$")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.axhline(C1 + C2, color='green', linestyle=':', label='Parallel (Saturation)')
    plt.axhline(C1 - C2, color='red', linestyle=':', label='Anti-Parallel (Zero Field)')
    plt.legend()
    plt.show()

simulate_magnetic_conductance()
#%%


# Your 18D Hamiltonian function (already includes J1, J3, J_ex, D, and Zeeman)
def solve_nibr2_18D(Bx, Bz, J1, J3, J_ex, D):
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
    H_total = H_zeeman + H_anisotropy + H_lattice + H_tunnel
    return np.linalg.eigvalsh(H_total)

def calculate_conductance_with_hamiltonian():
    # --- Physical Parameters ---
    hbar = 6.5821e-13  # meV * s
    m0 = 5.6856e-32    # mass of electron
    d = 6.200           # Thickness (Angstroms)
    E_fermi = 250.0    # Lead Fermi Energy (meV)
    V_offset = 500.0   # Static barrier height (meV)
    T_kelvin = 4.2     # Cryostat temperature
    kb = 0.08617       # meV/K
    
    # Magnetic Params
    J1, J3, J_ex, D = -1.56, 0.41, 0.2, 0.15
    Bx_fields = np.linspace(-9, 9, 100)
    
    conductance_list = []
    
    for B in Bx_fields:
        # 1. Solve the 18D Hamiltonian for this field
        energies = solve_nibr2_18D(B, 0, J1, J3, J_ex, D)
        
        # 2. Calculate the Thermal Average Energy <E> 
        # This represents the 'average state' of the NiBr2 monolayer
        weights = np.exp(-(energies - np.min(energies)) / (kb * T_kelvin))
        avg_spin_energy = np.sum(energies * weights) / np.sum(weights)
        
        # 3. Use <E> to modulate the Tunneling Barrier V0
        V_eff = V_offset + avg_spin_energy
        
        # 4. Calculate Transmission T using PDF Eq. 1.28
        alpha = np.sqrt(2 * m0 * (V_eff - E_fermi)) / hbar
        prefactor = (V_eff**2) / (4 * E_fermi * (V_eff - E_fermi))
        T = 1 / (1 + prefactor * (np.sinh(alpha * d))**2)
        
        conductance_list.append(T)

    # --- Plotting ---
    plt.figure(figsize=(9, 5))
    
    # Normalizing so the peak is at 1.0 is common for 'Arbitrary Units'
    G_plot = np.array(conductance_list) / np.max(conductance_list)
    
    plt.plot(Bx_fields, G_plot, color='blue', lw=2)
    plt.title("Normalized Conductance via 18D Spin Hamiltonian")
    plt.xlabel("In-Plane Magnetic Field $B_x$ (T)")
    plt.ylabel("Conductance $G/G_{max}$ (Arbitrary Units)")
    plt.grid(True, alpha=0.3)
    plt.show()

calculate_conductance_with_hamiltonian()
#%%

def solve_nibr2_lattice(Lx, Ly, Bx, Bz, J1, J3, D=0.15):
    N = Lx * Ly
    g_ni = 2.21
    mu_B = 0.05788
    
    # Base S=1 operators
    sz = sparse.csr_matrix([[1, 0, -1]]) # This is wrong in your snippet, should be:
    sz = sparse.diags([1, 0, -1])
    sp = sparse.csr_matrix([[0, np.sqrt(2), 0], [0, 0, np.sqrt(2)], [0, 0, 0]])
    sm = sp.getH()
    sx = (sp + sm) / 2
    sy = (sp - sm) / 2j
    id_s = sparse.eye(3)

    def get_op(op, site_idx):
        """Constructs a global operator for a specific site"""
        op_list = [id_s] * N
        op_list[site_idx] = op
        full_op = op_list[0]
        for i in range(1, N):
            full_op = sparse.kron(full_op, op_list[i], format='csr')
        return full_op

    H = sparse.csr_matrix((3**N, 3**N))

    # 1. Zeeman & Anisotropy (Single Site Terms)
    for i in range(N):
        Si_x = get_op(sx, i)
        Si_z = get_op(sz, i)
        H += g_ni * mu_B * (Bx * Si_x + Bz * Si_z)
        H += D * (Si_z ** 2)

    # 2. Exchange (Two-Site Terms)
    # Define your 2D grid logic here to find neighbors
    for i in range(N):
        x, y = i // Ly, i % Ly
        # Example: Nearest Neighbor J1 (Right and Down)
        neighbors = []
        if x + 1 < Lx: neighbors.append(i + Ly)
        if y + 1 < Ly: neighbors.append(i + 1)
        
        for j in neighbors:
            # S_i . S_j interaction
            for op in [sx, sy, sz]:
                H += J1 * (get_op(op, i) @ get_op(op, j))

    # Solve for the lowest few eigenvalues (k=6)
    vals, vecs = eigsh(H, k=6, which='SA')
    return vals
