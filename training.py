#!/usr/bin/env python3

#this script will transform labeled data into .npz files for training

import os
import numpy as np
from ase.io import read
import glob
from gmnn.trainer import PESTrainer

HARTREE_TO_KCAL_MOL = 627.5094740631  # Hartree to kcal/mol conversion factor

#function to count subdirectories in a given directory
def count_subdirectories(directory):
    return sum(os.path.isdir(os.path.join(directory, entry)) for entry in os.listdir(directory))


#function looping though all subdirectories and respective *.xyz files to load them to atoms objects and extract data
def prep_set(directory, n_maxat, dataset_name='dataset.npz'):
    n_data = count_subdirectories(directory)

    # numpy arrays
    R = np.zeros((n_data, n_maxat, 3), dtype=np.float64)    # Cartesian coordinates
    F = np.zeros((n_data, n_maxat, 3), dtype=np.float64)    # atomic forces
    E = np.zeros((n_data, ), dtype=np.float64)              # total energies
    C = np.zeros((n_data, 3, 3), dtype=np.float64)          # periodic cell
    Z = np.zeros((n_data, n_maxat), dtype=np.int64)         # atomic numbers
    N = np.zeros((n_data, ), dtype=np.int64)                # number of atoms

    # loop over all subdirectory/final*xyz, using glob
    for i, filepath in enumerate(glob.glob(os.path.join(directory, '*/final*.xyz'))):
        atoms = read(filepath)
        natoms = len(atoms)

        # extract data
        R[i, :natoms, :] = atoms.get_positions()
        F[i, :natoms, :] = atoms.get_forces() * HARTREE_TO_KCAL_MOL
        E[i] = atoms.get_total_energy() * HARTREE_TO_KCAL_MOL
        C[i, :, :] = atoms.get_cell()
        Z[i, :natoms] = atoms.get_atomic_numbers()
        N[i] = natoms

    np.savez(dataset_name, R=R, F=F, E=E, C=C, Z=Z, N=N)

#function to prepare pes_training.txt before running this script, based on previous .txt file 
def write_pes_training_file(filename='pes_training.txt', params: dict):
    """
    Write a pes_training.txt file with given parameters.

    Args:
        filename: output file path
        params: dict with key -> value, written as '--key=value'
    """
    with open(filename, "w") as f:
        for key, value in params.items():
            f.write(f"--{key}={value}\n")



if __name__ == "__main__":

    prep_set('calculations', n_maxat=210, dataset_name='dataset.npz')

    params = {
    "data_path": "dataset.npz",
    "model_path": "models",
    "model_name": "clusters",
    "cutoff": 5.5,
    "n_train": 16800,
    "n_valid": 2200,
    "n_test": 2200,}

    write_pes_training_file("pes_training.txt", params)

    trainer = PESTrainer(config="pes_training.txt")
    trainer.fit()
    trainer.eval()

