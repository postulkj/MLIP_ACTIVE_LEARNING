# **MLIP Active Learning**

> **Status:** Work in Progress  
> This repository is under active development. Core functionality is being integrated and tested. Interfaces, file structures, and configurations may change.

A framework for **active learning of machine-learning interatomic potentials (MLIPs)** using **Gaussian Moments Neural Networks (GMNN)**.

---

## **Overview**

This project implements an automated workflow for iterative training and refinement of MLIPs.  
The system performs:

1. Initial training of a GMNN potential on a small labeled dataset.  
2. Estimation of uncertainties on unlabeled configurations.  
3. Selection of new informative samples for labeling.  
4. Model retraining with the expanded dataset.  

The goal is to obtain accurate interatomic potentials with a minimal number of expensive reference calculations.

---

## **Current Status**

- GMNN-based model training functional.  
- Full active learning loop implemented in `control.py`.  
- Data selection, labeling, and result management modules operational.

---

## **Project Structure**

```text
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
```
## **Requirements**

- Python 3.10  
- GMNN (Gaussian Moments Neural Network)  
- ASE (Atomic Simulation Environment)  

All other dependencies (TensorFlow, NumPy, etc.) are managed within GMNN.

---

## **Usage**

Once GMNN is available in the environment, the workflow runs in two stages.

### **1. Initial Training**

```bash
python scripts/control.py
```
Configuration is loaded as:

```python
cfg = load_config("config/init_config.txt")
```

Trains the initial GMNN potential using the starting labeled dataset.

### **2. Active Learning Loop** *(in development)*

Subsequent iterations are controlled by:

```python
cfg = load_config("config/al_config.txt")
```

This stage is currently under development.
It will perform uncertainty evaluation on unlabeled data, select new configurations for labeling, and retrain the model on the updated dataset once integrated.

## **Future Work**

- Finalize implementation of the active learning loop in `control.py`  
- Automate model retraining and dataset updates  
- Add extended logging and performance monitoring  
- Expand compatibility with additional MLIP architectures and datasets  
- Prepare documentation and example workflows for reproducibility
