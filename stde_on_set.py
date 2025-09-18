#!/home/postulka/programs/anaconda3/bin/python

import numpy as np
from ase import Atoms
from gmnn.calculators import ASECalculator

HARTREE_TO_KCALMOL = 627.51

def build_atoms(positions, atomic_numbers):
    mask = np.array(atomic_numbers) != 0.0
    Z_clean = np.array(atomic_numbers)[mask]
    pos_clean = np.array(positions)[mask]
    return Atoms(numbers=Z_clean, positions=pos_clean)

def init_calculator(atoms, model_path, config_file):
    return ASECalculator(
        atoms=atoms,
        model_path=model_path,
        config=config_file,
        device_number=0,
        use_all_features=True,
        wrap_positions=False,
        compute_stress=False,
        set_units="kcal/mol to Hartree",
    )

def compute_stde_for_atoms(calc, atoms):
    atoms.set_calculator(calc)
    var_f = calc.get_force_variance(atoms) * HARTREE_TO_KCALMOL
    stde_f = np.sqrt(var_f).mean()
    var_e = calc.get_energy_variance(atoms) * HARTREE_TO_KCALMOL
    stde_e = np.sqrt(var_e)
    return stde_e, stde_f

def mean_diff_force(atoms, calc, ref_forces):
            forces_calc = atoms.get_forces()*HARTREE_TO_KCALMOL
            diff_forces = abs(ref_forces - forces_calc)
            f_mean = np.abs(np.array(forces_calc)).mean()
            return f_mean


if __name__ == "__main__":
    data_file = '../../moved_filtered_clusters.npz'
    model_path = '/home/postulka/HF_BROKEN_SYMMETRY/TRAIN/acetaldehyde/models/move_size_7500'
    config_file = 'pes_move_size_7500.txt'
    output_file = 'stde_results.txt'

    data = np.load(data_file, allow_pickle=True)
    R, Z, N, E, F = data["R"], data["Z"], data["N"], data["E"], data["F"]

    with open(output_file, 'w') as f_out:
        f_out.write("#Structure index, natom, stde energy, stde forces, energy error, forces error\n")
        natom = None
        calc = None
        for i in range(len(N)):
            atoms = build_atoms(R[i], Z[i])
            if i == 0:
                natom = len(atoms)
                calc = init_calculator(atoms, model_path, config_file)
                continue
            if len(atoms) != natom:
                natom = len(atoms)
                calc = init_calculator(atoms, model_path, config_file)
            stde_e, stde_f = compute_stde_for_atoms(calc, atoms)
            energy_ref = E[i]
            energy_calc = atoms.get_potential_energy()*HARTREE_TO_KCALMOL
            diff_energy = abs(energy_ref-energy_calc)
            forces_ref = data["F"][i][0:natom]
            diff_force = mean_diff_force(atoms, calc, forces_ref)
            f_out.write(f"{i} {natom} {stde_e} {stde_f} {diff_energy} {diff_force}\n")

