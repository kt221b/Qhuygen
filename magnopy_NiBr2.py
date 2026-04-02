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

spinham.add(nus = [(0,0,0),(0,0,0)], alphas=(0,0), parameter= np.diag([0,0,0.3]))
spinham.add(nus = [(0,0,0),(1,0,0)], alphas=(0,0), parameter= 1.2*np.eye(3), populate_equivalent=True)
spinham.add(nus = [(0,0,0),(0,1,0)], alphas=(0,0), parameter= 1.2*np.eye(3), populate_equivalent=True)
spinham.add(nus = [(0,0,0),(1,1,0)], alphas=(0,0), parameter= 1.2*np.eye(3), populate_equivalent=True)

pe1, pe2 = magnopy.experimental.plot_spinham(spinham=spinham)
pe1.save(output_name="pe1.html", axes_visible=False, width= 1000, height=1000)
pe2.save(output_name="pe2.html", axes_visible=False, width= 1000, height=1000)

# Create Energy object and Optimize
# energy = magnopy.Energy(spinham)

# optimize()




