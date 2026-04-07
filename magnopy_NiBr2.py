# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 13:36:37 2026

@author: Principal
"""
import numpy as np
import matplotlib.pyplot as plt
import magnopy 
print(magnopy.__file__)

# 1. Define the Cell (NiBr2 parameters)
a, c = 3.70, 6.26
cell = np.array([
    [a, 0, 0],
    [-0.5 * a, (np.sqrt(3) / 2) * a, 0],
    [0, 0, c]
])

# 2. Define the Atoms dictionary (required structure)
atoms = {
    "names": ["Ni"],
    "species": ["Ni"],
    "spglib_types": [1],
    "positions": [[0.0, 0.0, 0.0]],
    "spins": [1.0],      # Ni2+ S=1
    "g_factors": [2.0]
}

# 3. Set the Convention
# Using the specific parameters you provided
convention = magnopy.Convention(
    multiple_counting=True, 
    spin_normalized=False, 
    c1=1, c21=1, c22=1
)

# 4. Initialize Hamiltonian
spinham = magnopy.SpinHamiltonian(cell=cell, atoms=atoms, convention=convention)

# spinham.add(nus = [(0,0,0),(0,0,0)], alphas=(0,0), parameter= np.diag([0,0,0.3]))
# spinham.add(nus = [(0,0,0),(1,0,0)], alphas=(0,0), parameter= 1.2*np.eye(3), populate_equivalent=True)
# spinham.add(nus = [(0,0,0),(0,1,0)], alphas=(0,0), parameter= 1.2*np.eye(3), populate_equivalent=True)
# spinham.add(nus = [(0,0,0),(1,1,0)], alphas=(0,0), parameter= 1.2*np.eye(3), populate_equivalent=True)
# --- Magnetic Parameters ---
# J values (in meV)
j1 = 3.19   # Ferromagnetic
j2 = 0.0    # Often small/neglected in NiBr2, but added here for completeness
j3 = -1.56   # Antiferromagnetic (Drives the helimagnetism)
K  = 0.1    # Easy-plane (Hard-axis Z)

# 1. On-site Anisotropy (21 group equivalent)
spinham.add(nus=[(0,0,0), (0,0,0)], alphas=(0,0), parameter=np.diag([0, 0, K]))

# 2. J1: Nearest Neighbors
# Your (1,1,0) is correct for the third direction in this basis
j1_params = j1 * np.eye(3)
spinham.add(nus=[(0,0,0), (1,0,0)], alphas=(0,0), parameter=j1_params, populate_equivalent=True)
spinham.add(nus=[(0,0,0), (0,1,0)], alphas=(0,0), parameter=j1_params, populate_equivalent=True)
spinham.add(nus=[(0,0,0), (1,1,0)], alphas=(0,0), parameter=j1_params, populate_equivalent=True)

# 3. J2: Second-Nearest Neighbors
j2_params = j2 * np.eye(3)
spinham.add(nus=[(0,0,0), (2,1,0)], alphas=(0,0), parameter=j2_params, populate_equivalent=True)
spinham.add(nus=[(0,0,0), (1,2,0)], alphas=(0,0), parameter=j2_params, populate_equivalent=True)
spinham.add(nus=[(0,0,0), (1,-1,0)], alphas=(0,0), parameter=j2_params, populate_equivalent=True)

# 4. J3: Third-Nearest Neighbors
# These are essential for the helimagnetic state in NiBr2
j3_params = j3 * np.eye(3)
spinham.add(nus=[(0,0,0), (2,0,0)], alphas=(0,0), parameter=j3_params, populate_equivalent=True)
spinham.add(nus=[(0,0,0), (0,2,0)], alphas=(0,0), parameter=j3_params, populate_equivalent=True)
spinham.add(nus=[(0,0,0), (2,2,0)], alphas=(0,0), parameter=j3_params, populate_equivalent=True)


pe1, pe2 = magnopy.experimental.plot_spinham(spinham=spinham)
pe1.save(output_name="pe1.html", axes_visible=False, width= 1000, height=1000)
pe2.save(output_name="pe2.html", axes_visible=False, width= 1000, height=1000)

# Create Energy object and Optimize
energy=magnopy.Energy(spinham)

# Define test spin configurations (Spin Directions)
# Format: [[Sx, Sy, Sz]] because there is 1 Ni atom per unit cell
sd_x = [[1, 0, 0]]  # Spin pointing along X
sd_y = [[0, 1, 0]]  # Spin pointing along Y
sd_z = [[0, 0, 1]]  # Spin pointing along Z (Hard axis)

# Compute and print classical energies (Default: meV)
e_x = energy(sd_x)
e_y = energy(sd_y)
e_z = energy(sd_z)

print("--- NiBr2 Unit Cell Energies ---")
print(f"Energy (Spin || X): {e_x:.4f} meV")
print(f"Energy (Spin || Y): {e_y:.4f} meV")
print(f"Energy (Spin || Z): {e_z:.4f} meV")

# Verification of Easy-Plane Anisotropy
if e_z > e_x:
    print("\nResult: Z is the Hard Axis (Easy-plane confirmed).")
if e_y > e_z:
    print("\nResult: Y is the Hard Axis (Easy-plane confirmed).")
else:
    print("\nResult: Check anisotropy sign/parameter.")
#%%  optimization


# 5) Create the Supercell
# Note: It's a standalone function where you pass the original spinham
supercell_shape = (20, 20, 1)
new_spinham = magnopy.make_supercell(spinham=spinham, supercell=supercell_shape)

# 6) Optimization Setup
# In the latest versions, Energy often takes the Hamiltonian and manages its own state
energy = magnopy.Energy(new_spinham)
n_spins = len(new_spinham.atoms.names)
# Initialize and randomize
# If magnopy.State(new_spinham) fails, check if energy.randomize() exists
initial_state = np.random.normal(size=(n_spins, 3))
initial_state /= np.linalg.norm(initial_state, axis=1)[:, np.newaxis]
initial_state = initial_state.tolist()

print(f"Starting optimization for {n_spins} spins...")

# The optimize method returns the optimized spin configuration
# method='cg' (Conjugate Gradient) is usually the best for this
optimized_state = energy.optimize(initial_state, energy_tolerance=1e-6)
#%% plots
pos = np.array(new_spinham.atoms.positions)
x = pos[:, 0]
y = pos[:, 1]

# 2. Convert optimized_state to a NumPy array if it isn't one
# Shape should be (N_spins, 3)
S = np.array(optimized_state)
u = S[:, 0]  # Sx component
v = S[:, 1]  # Sy component
w = S[:, 2]  # Sz component (for coloring)

# 3. Create the 2D Map
plt.figure(figsize=(10, 8))

# Quiver plot: (x, y) are positions, (u, v) are the spin directions in-plane
# We color the arrows by their Z-component (w) to see if any point out-of-plane
q = plt.quiver(x, y, u, v, w, cmap='coolwarm', pivot='mid', scale=20)

# Add a colorbar to represent Sz (Out-of-plane component)
cbar = plt.colorbar(q)
cbar.set_label('Spin Z-component ($S_z$)')

# Formatting for the triangular lattice
plt.gca().set_aspect('equal')
plt.title('NiBr2 Optimized Spin Texture (20x20 Supercell)')
plt.xlabel('x ($\AA$)')
plt.ylabel('y ($\AA$)')
plt.grid(True, linestyle='--', alpha=0.5)

plt.show()