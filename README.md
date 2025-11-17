# Machine Learning-Guided Inverse Design of MOFs for High Usable Hydrogen Capacity Storage

This repository accompanies the article _"Machine Learning-Guided Inverse Design of MOFs for High Usable Hydrogen Capacity Storage"_ and contains the code, data and supplementary results required to reproduce the analysis and explore new materials satisfying Department of Energy (DOE) targets. Everything needed to regenerate the figures, metrics and tables of the main text and the Supplementary Information (SI) is provided here.

## 🗂️ Repository Structure
```
ml-mofs-hydrogen-storage/
├── data/
│   └── structuralparameters-vs-capacities-h2.dat
├── src/
│   ├── run_all.py
│   ├── run_regression.py
│   ├── diagnostics.py
│   ├── bootstrap_confidence_intervals.py
│   └── utils.py
├── results/
│   ├── metrics.json, diagnostic_metrics.csv, bootstrap_*.csv
│   ├── parity_*.png, residuals_*.png (generated locally, not tracked)
│   └── … (plots, metrics, etc.; model binaries are generated locally)
├── README.md
└── environment.yml
```

## 🚀 Quick start
1. Install dependencies with `pip install -r requirements.txt` (or `conda env create -f environment.yml`).
2. Run the full pipeline:
   ```bash
   python -m src.run_all
   ```
   This trains all models, writes the diagnostics under `results/` (parity and residual PNG plots, CSV metrics, and bootstrap
   confidence intervals), and saves the local model binaries (not committed to the repo). PNG figures are generated locally and
   not committed to keep the repository free of binary files.

### 📏 Evaluation protocol
**Evaluation protocol.** Final performance was assessed on the held-out test set using the coefficient of determination (R<sup>2</sup>) and Mean Absolute Error (MAE). We report point estimates in the main text; 95% confidence intervals via bootstrap (1,000 resamples) and additional diagnostics (residual plots vs. predictions and vs. key features, learning curves, and y-scrambling tests) are provided in the Supplementary Information (SI). Physical plausibility was checked post hoc against known constraints on descriptors and trends from the literature.

## 🎯 Objectives

This work focuses on predicting structural parameters of Metal-Organic Frameworks (MOFs) that satisfy the following hydrogen storage targets:

### Target 1: DOE 2025
- Usable gravimetric capacity: `ugc = 5.5 wt. %`
- Usable volumetric capacity: `uvc ≥ 0.040 kg/L`

### Target 2: Double Tank Volume (System-level strategy)
- Usable gravimetric capacity: `ugc = 5.5 wt. %`
- Usable volumetric capacity: `uvc ≥ 0.020 kg/L`

### Target 3: Relaxed gravimetric condition
- Usable gravimetric capacity: `ugc ≥ 2.75 wt. %`
- Usable volumetric capacity: `uvc ≥ 0.020 kg/L`

All models were trained on a dataset of 106 simulated MOFs using GCMC (Grand Canonical Monte Carlo) simulations and were designed to generalize to unseen structures via extrapolation and inverse design.

---

## 🧠 Methodology Summary

The pipeline consists of:

- Classical and regularized linear regression (Ridge, Lasso)
- Controlled extrapolation by range expansion
- Physical, strict and qualitative constraints
- Evaluation on extrapolated samples
- Filtering and ranking of realistic candidates

### Key structural descriptors:
- `density` (kg/L)
- `porosity` (unitless)
- `Ri`: average pore radius (Å)
- `SSA`: specific surface area (m²/g)
- `SPV`: specific pore volume (cm³/g)

### Constraints applied:
- `0.3 ≤ density ≤ 3.0` kg/L (preferred: `0.1 ≤ density ≤ 0.6`)
- `0.3 ≤ porosity ≤ 0.9` (preferred: `0.5 ≤ porosity ≤ 0.8`)
- `5 Å ≤ Ri ≤ 15 Å`
- `SSA ≥ 4000 m²/g` (max 6000)
- `SPV ≥ 1.0 cm³/g` (max 2.0)

---

## 📊 Key Results

### ✅ Target: DOE 2025 (5.5 wt. %, ≥ 0.04 kg/L)
| Density | Porosity | Ri (Å) | SSA (m²/g) | SPV (cm³/g) | ugc (wt. %) | uvc (kg/L) |
|---------|----------|--------|------------|-------------|--------------|------------|
| 0.5999  | 0.7891   | 14.7784| 6000       | 1.0001      | ≈ 5.5        | ≈ 0.034    |

→ Volumetric capacity is slightly below DOE target.

### ✅ Target: Double Tank Volume (Relaxed `uvc`, fixed `ugc`)
| Density | Porosity | Ri (Å) | SSA (m²/g) | SPV (cm³/g) | ugc (wt. %) | uvc (kg/L) |
|---------|----------|--------|------------|-------------|--------------|------------|
| 0.3000  | 0.5000   | 15.000 | 6000       | 2.0000      | ≈ 5.14       | ≈ 0.0168   |

→ Both capacities slightly below relaxed targets.

### ✅ Target: Double Heavy Tank (Relaxed `ugc`)
| Density | Porosity | Ri (Å) | SSA (m²/g) | SPV (cm³/g) | ugc (wt. %) | uvc (kg/L) |
|---------|----------|--------|------------|-------------|--------------|------------|
| 0.4201  | 0.7674   | 10.232 | 5000       | 1.3072      | ≈ 3.46       | ≈ 0.0200   |

→ Both targets met.

---

## 📁 Additional notes

- Trained models (generated locally): `ridge_model.joblib`, `lasso_model.joblib`, `rf_model.joblib` (ignored by Git).
- Test metrics and coefficients: `metrics.json`, `ridge_coefficients.csv`, `rf_feature_importances.csv`.
- Bootstrap confidence intervals: `bootstrap_intervals.json` and `bootstrap_*.csv` files.
- Diagnostics and figures: `parity_*.png`, `residuals_*.png`, and `diagnostic_metrics.csv`. The four PNGs (parity and residual
  plots for Ridge and Lasso) are produced by `python -m src.run_all` and saved to `results/`; they are not tracked in Git to
  comply with binary file restrictions. After running the command locally, open:
  - `results/parity_ridge_ugc.png`
  - `results/residuals_ridge_ugc.png`
  - `results/parity_lasso_uvc.png`
  - `results/residuals_lasso_uvc.png`

---

## 📚 Citation

If you use this repository, please cite it as:

```bibtex

@misc{hernando2025mlmofs,
  author = {Francisco Hernando Gallego and Iván Cabria and Alejandra Granja-DelRío},
  title = {Machine Learning-Guided Inverse Design of MOFs for High Usable Hydrogen Capacity Storage},
  year = {2025},
  howpublished = {\url{https://github.com/fhernandogallego/ml-mofs-hydrogen-storage}},
  note = {GitHub repository}
}

```

---

## 📎 Supplementary Information

The supplementary information (SI) for this work is entirely contained within this repository and includes:

- Full technical description (below)
- Final regression results
- Figures and capacity tables
- Dataset and candidate configurations

### Diagnostic figures (generated locally)

Running `python -m src.run_all` produces four PNG figures in `results/` that support the SI discussion:

- **Ridge parity plot (`parity_ridge_ugc.png`)** – predicted vs. true usable gravimetric capacity (ugc) with the 45° reference
  line, showing the tight agreement of the Ridge model on the held-out test set.
- **Lasso parity plot (`parity_lasso_uvc.png`)** – predicted vs. true usable volumetric capacity (uvc), illustrating the lower
  but acceptable fit for the volumetric target.
- **Ridge residuals (`residuals_ridge_ugc.png`)** – residuals vs. predicted ugc, confirming no dominant bias and well-behaved
  dispersion around zero.
- **Lasso residuals (`residuals_lasso_uvc.png`)** – residuals vs. predicted uvc, used to diagnose variance patterns for the
  volumetric model.

These plots are regenerated locally (not versioned) and belong to the SI diagnostics referenced in the evaluation protocol.

---

## 📄 Appendix: Full Technical Description

# Machine Learning Methodology for Optimizing Hydrogen Storage Materials

### Methodology Overview

This repository applies regression models with domain-specific constraints to meet two hydrogen storage targets:

1. **Double tank targets:** `usablevc ≥ 0.020 kg/L` and `usablegc = 5.5 wt. %`.
2. **2025 targets:** `usablevc ≥ 0.040 kg/L` and `usablegc = 5.5 wt. %`.

The models use a dataset of 106 materials characterized by `density`, `porosity`, `Ri`, `SSA`, and `specific pore volume`, combined with physical, strict, and qualitative constraints to keep predictions realistic.

---

### Mathematical Framework

Linear regression models a dependent variable `y` as a weighted sum of input features plus an error term:

`y = beta_0 + beta_1 * x_1 + ... + beta_p * x_p + epsilon`

Here `y` is the target (e.g., usablegc or usablevc), `x_i` are the input features (density, porosity, specific surface area, etc.), `beta_0` is the intercept, `beta_i` are the coefficients, and `epsilon` captures residual variability.

Coefficients are estimated by minimizing the residual sum of squares:

`RSS = Σ (y_i - y_hat_i)^2`

Regularization (Ridge or Lasso) penalizes large coefficients to reduce overfitting and keeps the solutions physically reasonable.

---

### Constraints

#### Physical Constraints
These constraints define the fundamental boundaries within which materials can exist:

- `usablegc ≥ 0.0`
- `usablevc ≥ 0.0`
- `0 kg/L < density`
- `0 ≤ porosity < 1`
- `Ri > 0.0`
- `SSA > 0.0`
- `specific pore volume > 0.0`

#### Strict or Better Constraints
These reflect the properties of materials suitable for gas storage:

- `0.01 kg/L ≤ density ≤ 0.6 kg/L`
- `0.5 ≤ porosity ≤ 0.8`
- `3 angstroms ≤ Ri ≤ 20 angstroms`
- `4000 m²/g ≤ SSA ≤ 10,000 m²/g`
- `1.0 cm³/g ≤ specific pore volume ≤ 3.0 cm³/g`

#### Qualitative Constraints
Empirical relationships guide the model to align with observed material properties:

- SSA and specific pore volume are inversely proportional to density.
- Porosity is inversely proportional to density.
- High porosity correlates with larger Ri values.
- SSA and porosity exhibit a linear correlation.

The densities of materials (e.g., MOFs) generally fall between 0.1–4.1 kg/L, consistent with data on natural and synthetic materials like lead (11.3 kg/L) and osmium (22.6 kg/L).

---

### Implementation Details

The methodology was applied to a dataset comprising the physical and chemical properties of 100 materials. Following preprocessing (normalization, outlier removal), the dataset was split into training (70%) and testing (30%) subsets. Model performance was evaluated using metrics such as the coefficient of determination (R²) and Mean Absolute Error (MAE).

Additionally, techniques like cross-validation and hyperparameter tuning (e.g., using grid search) ensured robustness and minimized overfitting.

---

### Results for Key Targets

#### Target 3: Double Tank Volume Targets
**Objectives**
- usablevc ≥ 0.020 kg/L
- usablegc = 5.5 wt. %

**Results**
- density: 0.3000
- porosity: 0.5000
- Ri: 15.0000 Å
- SSA: 6000.0 m²/g (upper limit met)
- specific pore volume: 2.0000 cm³/g

**Capacities**
- usablevc ≈ 0.0168 kg/L (below target)
- usablegc ≈ 5.14 wt. % (slightly below target)

#### Target 4: Double Heavy Tank Targets
**Objectives**
- usablevc ≥ 0.020 kg/L
- usablegc ≥ 0.5 wt. %

**Results**
- density: 0.4201
- porosity: 0.7674
- Ri: 10.2324 Å
- SSA: 5000.2 m²/g
- specific pore volume: 1.3072 cm³/g

**Capacities**
- usablevc ≈ 0.0200 kg/L (meets target)
- usablegc ≈ 3.46 wt. % (well above minimum)

