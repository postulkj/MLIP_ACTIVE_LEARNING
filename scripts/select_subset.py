import glob
import os
import random
from ase.io import read
from stde_on_set import init_calculator, compute_stde_for_atoms

def get_xyz_files(raw_dir):
    """Return a sorted list of all .xyz files in raw_dir."""
    return sorted(glob.glob(os.path.join(raw_dir, "*.xyz")))

def select_random_from_worst(xyz_files, n_select, model_path, config_file, pool_factor=2, stde_min=0.05):
    """
    Select a random sample from the worst (highest STDE) points, 
    but only consider points with STDE above stde_min.
    """
    stde_scores = []
    calc = None
    for xyz in xyz_files:
        atoms = read(xyz)
        if calc is None:
            calc = init_calculator(atoms, model_path, config_file)
        stde_e, _ = compute_stde_for_atoms(calc, atoms)
        if stde_e >= stde_min:
            stde_scores.append((xyz, stde_e))
    if not stde_scores:
        print(f"No points found with STDE >= {stde_min}.")
        return []
    stde_scores.sort(key=lambda x: x[1], reverse=True)
    pool_size = min(pool_factor * n_select, len(stde_scores))
    pool = [f for f, _ in stde_scores[:pool_size]]
    if len(pool) < n_select:
        print(f"Only {len(pool)} points in pool, returning all.")
        selected = pool
    else:
        selected = random.sample(pool, n_select)
    return selected

if __name__ == "__main__":
    RAW_DIR = "data/raw"
    N_SELECT = 20  # Number to select
    MODEL_PATH = "path/to/model"    # <-- Set this
    CONFIG_FILE = "path/to/config"  # <-- Set this
    POOL_FACTOR = 2                 # Pool is 2×N_SELECT worst
    STDE_MIN = 2.0                 # Minimum STDE threshold for selection

    xyz_files = get_xyz_files(RAW_DIR)
    selected_files = select_random_from_worst(
        xyz_files, N_SELECT, MODEL_PATH, CONFIG_FILE, pool_factor=POOL_FACTOR, stde_min=STDE_MIN
    )

    print("Randomly selected from the worst STDE (with STDE >= {:.3f}):".format(STDE_MIN))
    for fname in selected_files:
        print(fname)
