#!/usr/bin/env python3
import select_initial_set
import label
import os
import result_manager as rm
import training as trn
import shutil

def load_config(path: str) -> dict:
    cfg = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("--"):
                key, val = line[2:].split("=", 1)
                cfg[key.strip()] = val.strip()
    return cfg

def submit_training_job(config_file: str, script_file: str, job_name: str = "train_job"):
    shutil.copy(config_file, "temp_config.txt")
    """
    Submit a training job to the queue via qsub.
    
    Parameters:
    - config_file: Path to the config file for the training job.
    - script_file: Path to the Python training script to run.
    - job_name: Name of the job as it appears in the job scheduler.
    """
    # Ensure the job script is created
    job_script = f"""#!/bin/bash

# Run the training script
./{script_file}
    """
    
    # Save the job script to a file
    job_script_name = f"train_{job_name}.sh"
    with open(job_script_name, "w") as f:
        f.write(job_script)

    print(f"Training job script written to {job_script_name}")
    
    # Submit the job using qsub
    print(f"Submitting training job: {job_name} via qsub")
    os.system(f"qsub -cwd -V -q kq-gpu -pe shm 1 -l num_gpu=1 {job_script_name}")

if __name__ == "__main__":
    # load config file
    cfg = load_config("config/al_config.txt")

    raw_dir = cfg["data_path"] + "/raw"
    n_init  = int(cfg["initial_n"])
    n_max   = int(cfg["n_max_atoms"])
    out_npz = cfg["initial_npz"]

    # 1) initial selection
    files = select_initial_set.select_initial_set(raw_dir, n_init)

    # 2) labeling
    for f in files:
        label.label(f, "data/labeled", "template", submit_file="submit.sh", job_name="labeling_al")

    label.wait_for_calculations('labeling_al')

    # 3) harvest results
    os.makedirs("data/checked", exist_ok=True)
    os.makedirs("data/failed", exist_ok=True)

    pts = rm.list_points("data/labeled")
    res = rm.process_points(pts, -2000.0, -1500.0, molpro=False, orca=False)
    rm.move_points(res["passed"], "data/checked")
    rm.move_points(res["failed"], "data/failed")

    print(f"passed: {len(res['passed'])}, failed: {len(res['failed'])}")

    # 4) build dataset
    trn.prep_set("data/checked", n_maxat=n_max, dataset_name=out_npz)

    # 6) submit training job using qsub
    print("Submitting training job via qsub")
    submit_training_job(
        config_file="config/init_config.txt",   # config file for training
        script_file="scripts/submit_train.py",  # path to the Python training script
        job_name="train_al"  # job name for qsub
    )
    

    label.wait_for_calculations('train_al')

    print("Training done")

