import glob
import random
import numpy as np
from ase.io import read

def atomic_energy(atomic_numbers):
    # computes the sum of atomic energies to obtain cohesive energy
    dict = {
        "1":  -0.66782650788958,
        "6":  -37.9453942380145,
        "8":  -74.9579054924126
    }
    out = np.array([dict[str(key)] for key in atomic_numbers]).sum()
    return out

def select_initial_set(raw_dir, n_select, file_pattern="*.xyz"):
    """
    Select n_select files from raw_dir matching file_pattern and return their filenames.

    Args:
        raw_dir (str): Directory containing raw geometry files.
        n_select (int): Number of files to select.
        file_pattern (str): Pattern to match geometry files.

    Returns:
        list: List of selected file paths (relative or absolute).
    """
    files = glob.glob(f"{raw_dir}/{file_pattern}")

    if n_select > len(files):
        print(f"Warning: Requested {n_select} files, but only {len(files)} available. Selecting all available files.")
        n_select = len(files)

    selected = random.sample(files, n_select)
    return selected

def save_npz(selected_files, output_name="selected_initial_set.npz", n_maxat=210):
    n_data = len(selected_files)
    R = np.zeros((n_data, n_maxat, 3), dtype=np.float64)
    F = np.zeros((n_data, n_maxat, 3), dtype=np.float64)
    E = np.zeros((n_data, ), dtype=np.float64)
    C = np.zeros((n_data, 3, 3), dtype=np.float64)
    Z = np.zeros((n_data, n_maxat), dtype=np.int64)
    N = np.zeros((n_data, ), dtype=np.int64)

    for i_data, filepath in enumerate(selected_files):
        print(f"{i_data+1}/{n_data}: {filepath}")
        atoms = read(filepath)
        R[i_data, :len(atoms), :] = atoms.get_positions()
        F[i_data, :len(atoms), :] = atoms.get_forces() * 627.51
        E[i_data] = (atoms.get_total_energy() - atomic_energy(atoms.get_atomic_numbers())) * 627.51
        C[i_data] = atoms.get_cell()
        Z[i_data, :len(atoms)] = atoms.get_atomic_numbers()
        N[i_data] = len(atoms)

    np.savez(output_name, R=R, F=F, E=E, C=C, Z=Z, N=N)
    print(f"Saved {n_data} structures to {output_name}")

if __name__ == "__main__":
    RAW_DIR = "data/raw"
    N_SELECT = 10
    OUTPUT_FILE = "selected_initial_set.npz"
    N_MAXAT = 210

    selected_files = select_initial_set(RAW_DIR, N_SELECT)
    print(f"Selected {len(selected_files)} files:")
    for fname in selected_files:
        print(fname)
    save_npz(selected_files, output_name=OUTPUT_FILE, n_maxat=N_MAXAT)
