import os
import shutil
import glob
from ase.io import read

def list_points(dir_path):
    """
    List all point subdirectories in the given directory.
    """
    return [os.path.join(dir_path, d) for d in os.listdir(dir_path)
            if os.path.isdir(os.path.join(dir_path, d))]

def check_energy_range(point_dir, min_energy, max_energy):
    """
    Load results.xyz from point_dir and check if potential energy is within bounds.
    """
    xyz_path = os.path.join(point_dir, "results.xyz")
    if not os.path.exists(xyz_path):
        print(f"File {xyz_path} not found.")
        return False

    try:
        atoms = read(xyz_path)
        energy = atoms.get_potential_energy()
        return min_energy <= energy <= max_energy
    except Exception as e:
        print(f"Failed to process {xyz_path}: {e}")
        return False

def check_molpro_convergence(point_dir):
    """
    Check for Molpro convergence by searching 'QM1_s*out' for 'No convergence'.
    Returns True if converged (no 'No convergence' found), False otherwise.
    """
    out_files = glob.glob(os.path.join(point_dir, "QM1_s*out"))
    if not out_files:
        print(f"No Molpro output files found in {point_dir}")
        return False
    for out_file in out_files:
        with open(out_file, 'r', errors='ignore') as f:
            if 'No convergence' in f.read():
                print(f"No convergence found in {out_file}")
                return False
    return True

def check_orca_termination(point_dir):
    """
    Check for ORCA termination by searching 'QM2_s.com.out' for 'ORCA TERMINATED NORMALLY'.
    Returns True if terminated normally, False otherwise.
    """
    out_files = glob.glob(os.path.join(point_dir, "QM2_s.com.out"))
    if not out_files:
        print(f"No ORCA output files found in {point_dir}")
        return False
    for out_file in out_files:
        with open(out_file, 'r', errors='ignore') as f:
            if 'ORCA TERMINATED NORMALLY' not in f.read():
                print(f"ORCA did not terminate normally in {out_file}")
                return False
    return True

def process_points(point_dirs, min_energy, max_energy, molpro=False, orca=False):
    """
    Process a list of point directories, apply checks, and return dicts of results.
    If molpro=True, require Molpro convergence.
    If orca=True, require ORCA normal termination.
    """
    passed = []
    failed = []
    for dir_path in point_dirs:
        energy_ok = check_energy_range(dir_path, min_energy, max_energy)
        molpro_ok = True
        orca_ok = True
        if molpro:
            molpro_ok = check_molpro_convergence(dir_path)
        if orca:
            orca_ok = check_orca_termination(dir_path)
        if energy_ok and molpro_ok and orca_ok:
            passed.append(dir_path)
        else:
            failed.append(dir_path)
    return {'passed': passed, 'failed': failed}

def move_points(dirs, dest_root):
    """
    Move a list of point directories to a destination directory.
    """
    os.makedirs(dest_root, exist_ok=True)
    for src in dirs:
        dest = os.path.join(dest_root, os.path.basename(src))
        if os.path.exists(dest):
            print(f"Destination {dest} already exists. Skipping.")
            continue
        shutil.move(src, dest)
        print(f"Moved {src} -> {dest}")

if __name__ == "__main__":
    # User: Set these variables before running the script
    LABELED_DIR = "data/labeled"
    CHECKED_DIR = "data/checked"
    FAILED_DIR = "data/failed"
    MIN_E = -500.0
    MAX_E = 0.0
    MOLPRO = False  # Set to True if you want Molpro convergence check
    ORCA = False    # Set to True if you want ORCA termination check

    points = list_points(LABELED_DIR)
    results = process_points(points, MIN_E, MAX_E, molpro=MOLPRO, orca=ORCA)

    print("Moving passed points to checked:")
    move_points(results['passed'], CHECKED_DIR)
    print("Moving failed points to failed:")
    move_points(results['failed'], FAILED_DIR)
