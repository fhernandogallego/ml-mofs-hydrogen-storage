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
│   ├── ridge_model.joblib
│   ├── lasso_model.joblib
│   ├── rf_model.joblib
│   └── … (plots, metrics, etc.)
├── README.md
└── environment.yml
```

## 🚀 Quick start
1. Install dependencies with `pip install -r requirements.txt` (or `conda env create -f environment.yml`).
2. Run the full pipeline:
   ```bash
   python -m src.run_all
   ```
   All artifacts (trained models, metrics, bootstrap intervals, and figures) are saved under `results/`.

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
- Usable gravimetric capacity: `ugc ≥ 0.5 wt. %`
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

- Trained models: `ridge_model.joblib`, `lasso_model.joblib`, `rf_model.joblib`.
- Test metrics and coefficients: `metrics.json`, `ridge_coefficients.csv`, `rf_feature_importances.csv`.
- Bootstrap confidence intervals: `bootstrap_intervals.json` and `bootstrap_*.csv` files.
- Diagnostics and figures: `parity_*.png`, `residuals_*.png`, and `diagnostic_metrics.csv`.
- Example plot auto-generated by `python -m src.run_all`:

> Note: generated artifacts (e.g., PNG figures) are not versioned. Run `python -m src.run_all` to regenerate them under `results/` when needed.

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

---

## 📄 Appendix: Full Technical Description

# Machine Learning Methodology for Optimizing Hydrogen Storage Materials

### Methodology Overview

The optimization of hydrogen storage materials has been conducted using an advanced regression methodology inspired by recent breakthroughs in materials informatics [1]. This approach, combining linear regression techniques with domain-specific constraints, aligns closely with the techniques outlined in [2], where a combination of physical constraints and predictive modeling was used to optimize functional properties of materials.

The present work focuses on achieving two critical targets for hydrogen storage materials:

1. **Double tank targets:** `usablevc ≥ 0.020 kg/L` and `usablegc = 5.5 wt. %`.
2. **2025 targets:** `usablevc ≥ 0.040 kg/L` and `usablegc = 5.5 wt. %`.

These targets were approached by applying regression models to a dataset of 100 materials characterized by properties including `density`, `porosity`, `Ri`, `SSA`, and `specific pore volume`. The methodology integrates physical, strict, and qualitative constraints, ensuring realistic and physically achievable predictions.

---

### Mathematical Framework

Linear regression establishes a predictive relationship between a dependent variable \( y \) and a set of independent variables \( \mathbf{X} \). The model is expressed as:

\[
y = \beta_0 + \sum_{i=1}^{p} \beta_i x_i + \epsilon
\]

Where:
- \( y \): Dependent variable (e.g., usablegc or usablevc).
- \( x_i \): Independent variables (e.g., density, porosity, specific surface area).
- \( \beta_0 \): Intercept term.
- \( \beta_i \): Coefficients for each independent variable.
- \( \epsilon \): Error term capturing residual variability.

The coefficients \( \beta_i \) are estimated by minimizing the Residual Sum of Squares (RSS):

\[
RSS = \sum_{i=1}^{n} \left(y_i - \hat{y}_i\right)^2
\]

Here, \( y_i \) represents the observed values, and \( \hat{y}_i \) represents the predicted values based on the model.

To ensure the model aligns with the physical constraints of hydrogen storage materials, regularization techniques such as Ridge Regression or LASSO can be employed. These methods penalize large coefficients, reducing overfitting and enhancing interpretability.

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

The methodology was applied to a dataset comprising the physical and chemical properties of 100 materials. Following preprocessing (normalization, outlier removal), the dataset was split into training (70%) and testing (30%) subsets. Model performance was evaluated using metrics such as the coefficient of determination (\( R^2 \)) and Mean Absolute Error (MAE).

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

