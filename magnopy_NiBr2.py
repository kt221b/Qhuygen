# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 13:36:37 2026

@author: Principal
"""
# defining hamiltonian
import gc
import numpy as np
import matplotlib.pyplot as plt
import magnopy 
# print(magnopy.__file__)

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

# --- Magnetic Parameters ---
# J values (in meV)
j1 = -1.313   # Ferromagnetic
j2 = 0.016    # Often small/neglected in NiBr2, but added here for completeness
j3 = 0.496   # Antiferromagnetic (Drives the helimagnetism)
K  = 0.025    # Easy-plane (Hard-axis Z)
#from neutron diffraction paper
# j1 = 1.56   # Ferromagnetic
# j2 = -0.018    # Often small/neglected in NiBr2, but added here for completeness
# j3 = -0.457   # Antiferromagnetic (Drives the helimagnetism)
# K  = 0.15    # Easy-plane (Hard-axis Z)
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
#%%  supercell optimization


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
frac_pos = np.array(new_spinham.atoms.positions)

super_cell_matrix = np.array(new_spinham.cell)
cart_pos = frac_pos @ super_cell_matrix

x = cart_pos[:, 0]
y = cart_pos[:, 1]

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
q = plt.quiver(x, y, u, v, cmap='coolwarm', pivot='mid', scale=60)

# Add a colorbar to represent Sz (Out-of-plane component)
# cbar = plt.colorbar(q)
# cbar.set_label('Spin Z-component ($S_z$)')

# Formatting for the triangular lattice
plt.gca().set_aspect('equal')
plt.title('NiBr2 Optimized Spin Texture (2 0x20 Supercell)')
plt.xlabel('x ($\AA$)')
plt.ylabel('y ($\AA$)')
plt.grid(True, linestyle='--', alpha=0.5)

plt.show()

#%%
#making feild sweep for taking snapshot at each field 


# Define your field range
field_values = np.arange(-8, 9, 1)  # -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5
results = {}
g_factor = 2.0
mu_B = 0.05788     # meV/T
# Use the initial random state for the very first iteration

current_state = initial_state

for b_val in field_values:
    print(f"Running optimization for B_z = {b_val}...")

    # 1. Define the Zeeman matrix for the z-direction
    # [0, 0, b_val] targets the S_z component
    zeeman_param = g_factor * mu_B * b_val
    zeeman_matrix = np.diag([zeeman_param, 0, 0])
    
    # 2. Update the Hamiltonian
    # 'when_present="replace"' is key here to overwrite the previous field value
    new_spinham.add(
        nus=[(0,0,0), (0,0,0)], 
        alphas=(0,0), 
        parameter=zeeman_matrix, 
        populate_equivalent=True, 
        when_present="replace"
    )
    
    # 3. Setup Energy object
    energy = magnopy.Energy(new_spinham)
    
    # 4. Optimize
    # We pass 'current_state' so the spins don't have to re-randomize every time
    optimized_state = energy.optimize(current_state, energy_tolerance=1e-5)
    
    # 5. Store the result
    results[b_val] = optimized_state
    
    # Update current_state for the next field step (adiabatic tracking)
    current_state = optimized_state

print("Optimization sweep finished.")
#%%
frac_pos = np.array(new_spinham.atoms.positions)
super_cell_matrix = np.array(new_spinham.cell)
cart_pos = frac_pos @ super_cell_matrix

x = cart_pos[:, 0]
y = cart_pos[:, 1]

# 2. Iterate through the results dictionary
# Sorted ensures we go from -5 to 5 in order
for b_val in sorted(results.keys()):
    # Extract the state for this specific field
    S = np.array(results[b_val])
    
    u = S[:, 0]  # Sx
    v = S[:, 1]  # Sy
    w = S[:, 2]  # Sz (for color)

    # 3. Create the Plot
    plt.figure(figsize=(10, 8))
    
    # Use 'w' (Sz) for color to see out-of-plane tilting
    q = plt.quiver(x, y, u, v, cmap='coolwarm', pivot='mid', 
                   scale=60, width=0.005)

    plt.colorbar(q, label='Spin Z-component ($S_z$)')

    # Formatting
    plt.gca().set_aspect('equal')
    plt.title(f'Spin Texture at $B_z$ = {b_val}')
    plt.xlabel('x ($\AA$)')
    plt.ylabel('y ($\AA$)')
    plt.grid(True, linestyle='--', alpha=0.3)

    # Option A: Show each plot one by one
    plt.show()
#%%
def calculate_conductance_with_magnopy():
    # --- Physical Parameters ---
    hbar = 6.5821e-13  # meV * s
    m0 = 5.6856e-32    # mass of electron
    d = 6.26           # NiBr2 Thickness (Angstroms)
    E_fermi = 250.0    # Lead Fermi Energy (meV)
    V_offset = 500.0   # Static barrier height (meV)
    g_factor = 2.0
    mu_B = 0.05788     # meV/T
    
    # Range of Magnetic Fields
    Bx_fields = np.linspace(-8, 8, 40) # Start with fewer points as optimization takes time
    conductance_list = []
    global optimized_state
    supercell_shape = (20, 20, 1)
    new_spinham = magnopy.make_supercell(spinham=spinham, supercell=supercell_shape)
    # Initial state for the first optimization
    n_spins_actual = len(new_spinham.atoms.positions)
    current_state = optimized_state # Using your randomized state from the previous block

    print("Starting Magnetic Field Sweep...")

    for B in Bx_fields:
        # 1. Update Zeeman Term in the Hamiltonian
        # Zeeman energy = -g * mu_B * B * S_x
        # We add this as an on-site term (21 group)
        zeeman_param = g_factor * mu_B * B
        zeeman_matrix = np.diag([zeeman_param, 0, 0])
        
        # Clear previous field terms if necessary or just add/overwrite
        # Note: If your version doesn't support 'overwrite', you may need to recreate the spinham
        new_spinham.add(nus=[(0,0,0), (0,0,0)], alphas=(0,0), 
                        parameter=zeeman_matrix, populate_equivalent=True, when_present="replace")
        
        # 2. Re-optimize the state for the new field
        # Using the previous state as the starting point (warm start) speed up convergence
        energy_calc = magnopy.Energy(new_spinham)
        new_opt_state = energy_calc.optimize(current_state, energy_tolerance=1e-5, torque_tolerance=1e-05)
    
    # Update for next iteration
        current_state = new_opt_state
    
    # Calculate energy using the correct count
        total_energy = energy_calc(new_opt_state)
        avg_spin_energy = total_energy / n_spins_actual
        
        
        # 4. Modulate Tunneling Barrier
        V_eff = V_offset + avg_spin_energy
        
        # 5. Calculate Transmission T
        alpha = np.sqrt(2 * m0 * (V_eff - E_fermi)) / hbar
        prefactor = (V_eff**2) / (4 * E_fermi * (V_eff - E_fermi))
        T = 1 / (1 + prefactor * (np.sinh(alpha * d))**2)
        
        conductance_list.append(T)
        print(f"B = {B:.2f} T | Energy/site: {avg_spin_energy:.4f} meV | T: {T:.4e}")
        del energy_calc
        gc.collect()
    # --- Plotting ---
    plt.figure(figsize=(9, 5))
    G_plot = np.array(conductance_list) / np.max(conductance_list)
    plt.plot(Bx_fields, G_plot, 'o-', color='darkred', lw=2)
    plt.title("Conductance vs $B_x$ (Atomistic 30x30 Supercell)")
    plt.xlabel("Magnetic Field $B_x$ (T)")
    plt.ylabel("Normalized Conductance $G/G_{max}$")
    plt.grid(True, alpha=0.3)
    plt.show()

calculate_conductance_with_magnopy()