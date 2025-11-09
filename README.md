# MLIP Active Learning

Status: Work in Progress
This repository is under active development. Core functionality is being integrated and tested. Interfaces, file structures, and configurations may change.

A framework for active learning of machine-learning interatomic potentials (MLIPs) using Gaussian Moments Neural Networks (GMNN).

--- Overview

This project implements an automated workflow for iterative training and refinement of MLIPs. The system performs:
1) Initial training of a GMNN potential on a small labeled dataset.
2) Estimation of uncertainties on unlabeled configurations.
3) Selection of new informative samples for labeling.
4) Model retraining with the expanded dataset.

The goal is to obtain accurate interatomic potentials with a minimal number of expensive reference calculations.

--- Current Status

- GMNN-based model training functional.
- Full active learning loop implemented in control.py.
- Data selection, labeling, and result management modules operational.

--- Project Structure

MLIP_ACTIVE_LEARNING/
├── data/              # Raw, labeled, checked, and failed structures
├── scripts/           # Active learning and helper scripts
├── models/            # Trained GMNN models
├── templates/         # HPC submission templates
├── config/            # Configuration files
│   ├── init_config.txt    # Used for initial model training
│   └── al_config.txt      # Used for active learning iterations
├── tests/             # Basic tests
└── README.md

--- Requirements

- Python 3.10
- GMNN (Gaussian Moments Neural Network)
- ASE (Atomic Simulation Environment)

All other dependencies (TensorFlow, NumPy, etc.) are managed within GMNN.

--- Usage

Once GMNN is available in the environment, the workflow runs in two stages.

1) Initial Training
   Run:
   $ python scripts/control.py
   Configuration is loaded as:
   cfg = load_config("config/init_config.txt")
   Purpose:
   Trains the initial GMNN potential using the starting labeled dataset.

2) Active Learning Loop
   Subsequent iterations use:
   cfg = load_config("config/al_config.txt")
   Purpose:
   Performs uncertainty evaluation, selects new data for labeling, and retrains the model.

--- Future Work

- Extend uncertainty quantification methods
- Automate data selection strategies
- Add compatibility with other MLIP architectures
