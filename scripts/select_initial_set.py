import glob
import random

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

if __name__ == "__main__":
    RAW_DIR = "data/raw"
    N_SELECT = 500

    selected_files = select_initial_set(RAW_DIR, N_SELECT)
    print(f"Selected {len(selected_files)} files:")
    for fname in selected_files:
        print(fname)
