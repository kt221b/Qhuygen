# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 13:36:37 2026

@author: Principal
"""
import numpy as np
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
j1 = 1.2    # Ferromagnetic
j2 = 0.0    # Often small/neglected in NiBr2, but added here for completeness
j3 = -0.2   # Antiferromagnetic (Drives the helimagnetism)
K  = 0.3    # Easy-plane (Hard-axis Z)

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

#%%
# Create the Energy object for a 10x10 supercell
energy = magnopy.Energy(spinham, shape=(10, 10, 1))

# Initialize a state (this holds the spin vectors)
state = magnopy.State(spinham, shape=(10, 10, 1))

# Randomize spins to break symmetry and allow the spiral to form
state.randomize()

# Run the optimization
# This will update the 'state' object to the local minimum
energy.optimize(state, method='cg', tolerance=1e-6)

print(f"Final Energy: {energy.compute(state)} meV")

# Visualizing the optimized state
# This creates an interactive HTML plot of the spin vectors
ps = magnopy.experimental.plot_state(state=state)

# Save the spin texture visualization
ps.save(output_name="spin_texture.html", 
        width=1000, 
        height=1000, 
        quiver_scale=0.5) # Adjust quiver_scale to make arrows visible