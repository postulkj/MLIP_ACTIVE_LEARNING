
# Labeling script for calculation of molecular energy and gradients.

import os
import tempfile
from ase import Atoms
from ase.io import read, write


#labeling function taking *xyz file, working directory as an input
#calculating energy and gradients with external program in a temporary directory
def label(geom_file, workdir, submit_file,job_name="labeling_al"):
    # Read the geometry from the input file
    atoms = read(geom_file)

    # Create a directory for the calculation, based on the file name
    calc_dir = os.path.join(workdir, os.path.splitext(os.path.basename(geom_file))[0])
    os.makedirs(calc_dir, exist_ok=True)

    # Copy the geometry file and sumbit file to the calculation directory
    temp_geom_file = os.path.join(calc_dir, os.path.basename(geom_file))
    temp_submit_file = os.path.join(calc_dir, os.path.basename(submit_file))
    write(temp_geom_file, atoms)
    os.system(f'cp {submit_file} {temp_submit_file}')
    # qsub command to submit the job
    os.system(f'cd {calc_dir} && qsub -V -cwd -q $cpu -N {job_name} {temp_submit_file} && cd -')

    return

# Function to check if any calculation "labelling al" is running
def are_calculations_running(job_name):
    # Check the output of the qstat command for any job with the name "labeling_al"
    output = os.popen('qstat -u $USER').read()
    return job_name in output

# Function to wait until all calculations are finished
def wait_for_calculations(job_name):
    while are_calculations_running(job_name):
        time.sleep(60)  # Wait for 1 minute before checking again
    print("All calculations are finished. Proceeding...")
    return

# Example usage
if __name__ == "__main__":
    geom_file = "molecule.xyz"  # Input geometry file
    workdir = "./calculations"   # Working directory for calculations
    submit_file = "embedding.sh"    # Job submission script
    job_name = "labeling_al"  # Job name for the scheduler

    # Ensure the working directory exists
    os.makedirs(workdir, exist_ok=True)

    # Label the geometry
    result_atoms = label(geom_file, workdir, submit_file)

    # Wait for all calculations to finish before proceeding
    wait_for_calculations(job_name)

    # After calculations are done, read results (this part depends on how results are stored)
    # For example, if results are stored in a file named 'result.xyz' in the calc_dir:
    result_file = os.path.join(workdir, os.path.splitext(os.path.basename(geom_file))[0], 'result.xyz')
    if os.path.exists(result_file):
        result_atoms = read(result_file)
        print("Energy:", result_atoms.get_potential_energy())
        print("Forces:", result_atoms.get_forces())
    else:
        print("Result file not found.")
