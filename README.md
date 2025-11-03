# MLIP_ACTIVE_LEARNING
Pipeline for training and improving machine-learning interatomic potentials (MLIPs) using Gaussian Moments Neural Networks (GMNN) and an active learning loop.

## Project Structure

```
MLIP_ACTIVE_LEARNING/
│
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/         # Initial geometries (XYZ etc.)
│   ├── labeled/     # Successfully labeled/calculated results
│   ├── checked/     # Points after validity check (to be added to the training set)
│   └── failed/      # Failed or rejected calculations
│
├── scripts/
│   ├── select_initial_set.py
│   ├── label.py
│   ├── results_manager.py      # Combines checking, saving to labeled/failed
│   ├── train.py
│   ├── stde_on_set.py
│   ├── select_subset.py
│   └── active_learning_loop.py
│
├── models/
│
├── templates/
│   ├── submit.sh
│   └── embedding.sh
│
├── config/
│   └── pes_training.txt
│
└── tests/
```

**Key points:**  
- `data/` now has just `raw/`, `labeled/`, and `failed/`.
- `results_manager.py` will handle checking results and moving files to `labeled/` or `failed/`.
- No `utils/` directory.
- Everything else is streamlined for clarity.
