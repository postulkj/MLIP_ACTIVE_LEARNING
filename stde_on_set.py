#!/home/postulka/anaconda3/envs/gmnn_gpu/bin/python

#this script load .npz file with geometric data and computes stde for energy and forces for ecah structure

from gmnn.calculators import ASECalculator
import numpy as np

#loadd data
data = np.load('data.npz', allow_pickle=True)

R, Z, N, C, E = arrays["R"], arrays["Z"], arrays["N"], arrays["C"], arrays["E"]
#first atoms object from the set
index = 0
numb = [ i for i  in data["Z"][index] if i != 0.0 ]
pos = data["R"][index][0:len(numb)]  #[ j for i,j  in zip(data["Z"][index],data["R"][index]) if i != 0.0 ]
atoms = Atoms(numbers=numb, positions=pos)
#initialize calculator
calc = ASECalculator(atoms=atoms, model_path="/home/postulka/HF_BROKEN_SYMMETRY/TRAIN/acetaldehyde/models/just_energy", config="pes_just_energy.txt", device_number=0, use_all_features=True, wrap_positions=False, compute_stress=False, set_units="kcal/mol to kcal/mol")

#loop through the structures
for i in range(len(N)):
    numb = [ i for i  in data["Z"][index] if i != 0.0 ]
    pos = data["R"][index][0:len(numb)]  #[ j for i,j  in zip(data["Z"][index],data["R"][index]) if i != 0.0 ]
    atoms = Atoms(numbers=numb, positions=pos)
    atoms.set_calculator(calc)
    variance_f = calc.get_force_variance(atoms)
    stde_f = np.sqrt(variance).mean()
    variance_e = calc.get_energy_variance(atoms)
    stde_e = np.sqrt(variance)

    print(f"Index: {index}, STDE: {stde}")
    with open("stde_results.txt", "a") as f:
        f.write(f"{index} {stde}\n")
    


