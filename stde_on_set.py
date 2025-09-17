#!/home/postulka/programs/anaconda3/bin/python

#this script load .npz file with geometric data and computes stde for energy and forces for ecah structure
import numpy as np
from ase import Atoms

from gmnn.calculators import ASECalculator

def compute_stde(data_file, model_path, config_file, output_file='stde_results.txt'):
    HARTREE_TO_KCALMOL = 627.51
#loadd data
    data = np.load(data_file, allow_pickle=True)

    R, Z, N, C, E = data["R"], data["Z"], data["N"], data["C"], data["E"]

#loop through the structures
    with open(output_file, 'w') as f_out:
        for i in range(len(N)):
            numb = [ i for i  in data["Z"][i] if i != 0.0 ]
            pos = data["R"][i][0:len(numb)]  #[ j for i,j  in zip(data["Z"][index],data["R"][index]) if i != 0.0 ]
            atoms = Atoms(numbers=numb, positions=pos)
            if i == 0:
                natom=len(numb)
                calc = ASECalculator(atoms=atoms, model_path=model_path, config=config_file, device_number=0, use_all_features=True, wrap_positions=False, compute_stress=False, set_units="kcal/mol to Hartree")
                f_out.write("#Structure index, natom, stde energy, stde forces")
                continue
            if natom!=len(numb):
                natom = len(numb)
                calc = ASECalculator(atoms=atoms, model_path=model_path, config=config_file, device_number=0, use_all_features=True, wrap_positions=False, compute_stress=False, set_units="kcal/mol to Hartree")
            atoms.set_calculator(calc)
            variance_f = calc.get_force_variance(atoms)*HARTREE_TO_KCALMOL
            stde_f = np.sqrt(variance_f).mean()
            variance_e = calc.get_energy_variance(atoms)*HARTREE_TO_KCALMOL
            stde_e = np.sqrt(variance_e)
            f_out.write(f"{i} {natom} {stde_e} {stde_f}\n") 

if __name__ == "__main__":
    data_file = '../../moved_filtered_clusters.npz'
    compute_stde(data_file, f'/home/postulka/HF_BROKEN_SYMMETRY/TRAIN/acetaldehyde/models/move_size_7500', f'pes_move_size_7500.txt', output_file='stde_results.txt')
