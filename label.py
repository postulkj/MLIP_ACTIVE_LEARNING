#!/usr/bin/env python3
# Labeling script for calculation of molecular energy and gradients.

import os
import time
import glob
import shutil
from ase.io import read, write

def label(geom_file, workdir, template_dir, submit_file="submit.sh", job_name="labeling_al"):
    # Read geometry
    atoms = read(geom_file)

    # Create calculation directory
    calc_dir = os.path.join(workdir, os.path.splitext(os.path.basename(geom_file))[0])
    shutil.copytree(template_dir, calc_dir, dirs_exist_ok=True)

    # Write geometry file into calc_dir
    geom_dst = os.path.join(calc_dir, os.path.basename(geom_file))
    write(geom_dst, atoms)

    # Check that the specified submit file is in the template copy
    submit_path = os.path.join(calc_dir, submit_file)
    if not os.path.exists(submit_path):
        raise FileNotFoundError(f"{submit_file} not found in template: {submit_path}")

    # Submit the job
    os.system(f'cd {calc_dir} && qsub -V -cwd -q $cpu -N {job_name} {submit_file}')

    return calc_dir

def are_calculations_running(job_name):
    output = os.popen('qstat -xml -u postulka').read()
    return job_name in output

def wait_for_calculations(job_name):
    while are_calculations_running(job_name):
        time.sleep(60)
    print("All calculations are finished. Proceeding...")

if __name__ == "__main__":
    workdir = "./calculations"
    template_dir = "./template"
    submit_file = "submit.sh"   # Name of the job script inside template
    job_name = "labeling_al"

    os.makedirs(workdir, exist_ok=True)

    for geom_file in glob.glob("GEOMS/*.xyz"):
        label(geom_file, workdir, template_dir, submit_file, job_name)

    wait_for_calculations(job_name)

