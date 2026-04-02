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

#%%


def solve_nibr2_3x3_map(Bx, Bz, J1, J3, J_ex, D=0.6):
    Lx, Ly = 3, 3
    N = Lx * Ly
    g_ni, mu_B = 2.21, 0.05788   # mu_B = 0.05788	meV/T
    
    # Base Sparse Operators
    sz_s = sparse.diags([1, 0, -1]) # creates the Sz​ operator for a Spin-1 particle:
    sp_s = sparse.csr_matrix([[0, np.sqrt(2), 0], [0, 0, np.sqrt(2)], [0, 0, 0]]) #sp_s (S+): The raising operator. It moves a spin state "up" (e.g., from ∣−1⟩ to ∣0⟩).
    sx_s = (sp_s + sp_s.getH()) / 2   #sp_s.getH() The Hermitian adjoint of S+.
    sy_s = (sp_s - sp_s.getH()) / 2j
    id_s, id_e = sparse.eye(3), sparse.eye(2)
    
    # Pre-compute identity chain for speed
    def get_full_op(op, i):
        # i is the site index 0 to 8. Electron is index 9.
        if i < N:
            left = sparse.eye(3**i)
            right = sparse.eye(3**(N-i-1) * 2)
            return sparse.kron(left, sparse.kron(op, right), format='csr')
        else: # Electron site
            return sparse.kron(sparse.eye(3**N), op, format='csr')

    dim = (3**N) * 2
    H = sparse.csr_matrix((dim, dim), dtype=complex)

    # 1. Zeeman, Anisotropy, and Exchange
    print("Building Hamiltonian...")
    for i in range(N):
        Six, Siz = get_full_op(sx_s, i), get_full_op(sz_s, i)
        H += g_ni * mu_B * (Bx * Six + Bz * Siz)
        H += D * (Siz @ Siz)
        
        # Neighbor interactions (J1 and J3)
        r, c = i // Ly, i % Ly
        for dr, dc, J in [(0, 1, J1), (1, 0, J1), (0, 2, J3), (2, 0, J3)]:
            nr, nc = r + dr, c + dc
            if nr < Lx and nc < Ly:
                n_idx = nr * Ly + nc
                for op_base in [sx_s, sy_s, sz_s]:
                    H += J * (get_full_op(op_base, i) @ get_full_op(op_base, n_idx))

    # 2. Tunneling (Electron at index 9 couples to center Ni at index 4)
    center_ni = 4 
    sig_x = 2 * get_full_op(0.5 * sparse.csr_matrix([[0, 1], [1, 0]]), N)
    sig_y = 2 * get_full_op(0.5 * sparse.csr_matrix([[0, -1j], [1j, 0]]), N)
    sig_z = 2 * get_full_op(0.5 * sparse.diags([1, -1]), N)
    
    H += J_ex * (get_full_op(sx_s, center_ni) @ sig_x + 
                get_full_op(sy_s, center_ni) @ sig_y + 
                get_full_op(sz_s, center_ni) @ sig_z)

    # 3. Solve for Ground State
    print("Solving for Ground State...")
    vals, vecs = eigsh(H, k=1, which='SA')
    psi = vecs[:, 0]

    # 4. Compute expectations
    mx, my, mz = np.zeros((Lx, Ly)), np.zeros((Lx, Ly)), np.zeros((Lx, Ly))
    for i in range(N):
        r, c = i // Ly, i % Ly
        mx[r, c] = np.real(psi.conj().T @ get_full_op(sx_s, i) @ psi)
        my[r, c] = np.real(psi.conj().T @ get_full_op(sy_s, i) @ psi)
        mz[r, c] = np.real(psi.conj().T @ get_full_op(sz_s, i) @ psi)
    
    return mx, my, mz

# Execution and Plot
mx, my, mz = solve_nibr2_3x3_map(Bx=0, Bz=0, J1=-3.19, J3=1.56, J_ex=0.0)

plt.figure(figsize=(7, 6))
X, Y = np.meshgrid(np.arange(3), np.arange(3))
# Use Quiver for in-plane (x,y) and Color for out-of-plane (z)
st = plt.quiver(X, Y, mx, my, mz, cmap='coolwarm', pivot='middle', scale=2)
plt.colorbar(st, label='$\langle S_z \\rangle$ Projection')
plt.title("3x3 NiBr2 Ground State Spin Texture")
plt.xticks([0, 1, 2]); plt.yticks([0, 1, 2])
plt.show()

#%%


def simulate_nibr2_50x50(Lx=50, Ly=50, Bx=0, J1=-3.19, J3=1.56, D=0.60, steps=1000):
    # Initialize random spins on a 50x50 grid (Unit vectors in 3D)
    #Initialize random spins BUT kill the Z component immediately
    spins = np.random.normal(0, 1, (Lx, Ly, 3))
    spins[:, :, 2] = 0  # Force Sz to be zero at the start
    norms = np.linalg.norm(spins, axis=2, keepdims=True)
    spins /= (norms + 1e-9)
    
    g_ni, mu_B = 2.21, 0.05788
    external_field = np.array([Bx * g_ni * mu_B, 0.0, 0.0])

    for step in range(steps):
        # We use a copy to update all spins "simultaneously" (Jacobi-style)
        new_spins = spins.copy()
        
        # Vectorized neighbor sum for speed (Roll shifts the whole grid)
        # Nearest Neighbors (J1)
        neighbors_J1 = (np.roll(spins, 1, axis=0) + np.roll(spins, -1, axis=0) +
                        np.roll(spins, 1, axis=1) + np.roll(spins, -1, axis=1))
        
        # Third Nearest Neighbors (J3)
        neighbors_J3 = (np.roll(spins, 2, axis=0) + np.roll(spins, -2, axis=0) +
                        np.roll(spins, 2, axis=1) + np.roll(spins, -2, axis=1))
        
        # Effective Field: B_total = B_ext - J1*sum(S_nn) - J3*sum(S_3nn)
        # Note: D acts as a field pulling Sz toward 0 if D > 0 (Easy Plane)
        B_eff = external_field - (J1 * neighbors_J1) - (J3 * neighbors_J3)
        B_eff[:, :, 2] -= 2 * D * spins[:, :, 2]
        
        # Align spins with the local field
        mag = np.linalg.norm(B_eff, axis=2, keepdims=True)
        new_spins = B_eff / (mag + 1e-9)
        
        # Mixing/Damping to ensure smooth convergence
        spins = 0.1 * new_spins + 0.9 * spins
        
    return spins

# Run the simulation
# J3 must be > |J1|/4 to see the spiral!
spins_final = simulate_nibr2_50x50(Bx=0, J1=-3.19, J3=1.56, D=0.60)

# 2. Plotting the Texture
plt.figure(figsize=(10, 10))
# To keep the plot readable, we skip every 2nd arrow (subsampling)
sub = 2
X, Y = np.meshgrid(np.arange(0, 50, sub), np.arange(0, 50, sub))
u = spins_final[::sub, ::sub, 0]
v = spins_final[::sub, ::sub, 1]
color = spins_final[::sub, ::sub, 2] # Color by Sz

plt.quiver(X, Y, u, v, color, cmap='coolwarm', pivot='middle', scale=40)
plt.title(f"50x50 NiBr2 Spin Texture (Mean Field)\n$J_1=-3.19, J_3=1.56$ (Frustrated Spiral)")
plt.xlabel("Lattice X"); plt.ylabel("Lattice Y")
plt.show()

#%%
def simulate_nibr2_triangular(Lx=48, Ly=48, Bx=0.1, J1=-0.415, J3=0.614, D=0.15, steps=2000):
    # 1. Initialize spins in-plane (crucial for Panel a)
    spins = np.random.normal(0, 1, (Lx, Ly, 3))
    spins[:, :, 2] = 0 
    
    for step in range(steps):
        # 2. Triangular Neighbors (J1)
        # Standard square + the diagonal (bottom-left to top-right)
        neighbors_J1 = (np.roll(spins, 1, 0) + np.roll(spins, -1, 0) +
                        np.roll(spins, 1, 1) + np.roll(spins, -1, 1) +
                        np.roll(np.roll(spins, 1, 0), -1, 1) + 
                        np.roll(np.roll(spins, -1, 0), 1, 1))

        # 3. Third Neighbors (J3) - straight lines further out
        neighbors_J3 = (np.roll(spins, 2, 0) + np.roll(spins, -2, 0) +
                        np.roll(spins, 2, 1) + np.roll(spins, -2, 1))

        # 4. Field calculation with "Annealing" noise
        B_eff = -(J1 * neighbors_J1) - (J3 * neighbors_J3)
        B_eff[:, :, 2] -= 2 * D * spins[:, :, 2] # Easy-plane
        B_eff[:, :, 0] += Bx * 2.21 * 0.05788   # External field
        
        # Add cooling noise to find the "Stripe" ground state
        temp = 0.5 * (1 - step/steps)**2  # Quadratic decay
        B_eff += np.random.normal(0, temp, B_eff.shape)

        # 5. Normalize and Mix
        mag = np.linalg.norm(B_eff, axis=2, keepdims=True)
        spins = 0.2 * (B_eff / (mag + 1e-9)) + 0.8 * spins
        
    return spins
#%% color = spins_final[:, :, 1] # This shows the Sy component
spins_final = simulate_nibr2_triangular(Lx=48, Ly=48, Bx=30.0, steps=3000)


# 1. Prepare the triangular coordinates
Lx, Ly = 48, 48
x = np.arange(Lx)
y = np.arange(Ly)
X, Y = np.meshgrid(x, y)

# Shift coordinates for the triangular lattice look
X_tri = X + 0.5 * Y
Y_tri = Y * (np.sqrt(3) / 2)

# 2. Setup the Plot
plt.figure(figsize=(10, 10))

# A. Background: The smooth Sy stripes (Panel a style)
# We use pcolormesh here because it handles the skewed X_tri/Y_tri coordinates correctly
plt.pcolormesh(X_tri, Y_tri, spins_final[:, :, 1], cmap='coolwarm', shading='gouraud', alpha=0.8)

# B. Foreground: The Spin Arrows (Quiver)
# We subsample by 'skip' to keep the plot readable
skip = 2 
X_q = X_tri[::skip, ::skip]
Y_q = Y_tri[::skip, ::skip]
U_q = spins_final[::skip, ::skip, 0] # Sx component
V_q = spins_final[::skip, ::skip, 1] # Sy component

# pivot='middle' centers the arrow on the atom site
plt.quiver(X_q, Y_q, U_q, V_q, 
           color='black', 
           pivot='middle', 
           scale= 50,      # Adjust scale to make arrows larger/smaller
           width=0.003, 
           headwidth=3)

plt.gca().set_aspect('equal')
plt.axis('off')
plt.title("NiBr2 Spin Texture: Stripes with Quiver Overlay")
plt.show()


