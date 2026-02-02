# AdEase — Multilingual Traffic Forecasting

Overview
--------
AdEase is an ad-infrastructure company focused on maximizing clicks at minimum cost. This project analyzes historical Wikipedia page-view data (550 days for ~145k pages) to build scalable time-series forecasting pipelines across multiple languages and regions. The goal is to provide reliable forecasts to help optimize ad placement and budget allocation.

Contents
--------
- `adease-multilingual-traffic-forecasting.ipynb` — primary analysis notebook with EDA, feature engineering, model training (ARIMA, SARIMA, SARIMAX, Prophet), grid search, and recommendations.
- `data/train_1.csv` — page-level daily views (550 days).
- `data/Exog_Campaign_eng.csv` — exogenous campaign indicator time series (binary).

Key Highlights
--------------
- Exploratory analysis and parsing of Wikipedia page identifiers to extract language, access type, and origin.
- Missing-data handling (drop fully-empty series, threshold-based filtering, interpolation strategies).
- Time-series diagnostics: ADF tests, decomposition, ACF/PACF analysis, differencing and seasonality detection.
- Forecasting models implemented: ARIMA, SARIMA/SARIMAX (with exogenous), and Facebook Prophet.
- Pipeline to train, evaluate (MSE, MAE, MAPE), and visualize forecasts; includes a grid-search approach for ARIMA parameters.

Quickstart
----------
1. Create and activate a Python virtual environment (Windows example):

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install core dependencies (recommended):

```powershell
pip install numpy pandas matplotlib seaborn regex gdown langcodes iso639-lang plotly statsmodels scikit-learn prophet cmdstanpy joblib
```

Note: Installing `prophet` may require a working C++ toolchain or `cmdstanpy` backend. If you encounter issues on Windows, consider using Anaconda/Miniconda and installing `prophet` there.

3. Launch the notebook and run cells:

```powershell
pip install jupyterlab
jupyter lab
```

Open `adease-multilingual-traffic-forecasting.ipynb` and run the notebook top-to-bottom. The notebook contains setup cells to install packages and helper functions.

Usage and Reproducibility
------------------------
- Data: place `train_1.csv` and `Exog_Campaign_eng.csv` inside the `data/` folder (already present in this repository).
- The notebook loads data using `pd.read_csv('./data/train_1.csv')` and `pd.read_csv('./data/Exog_Campaign_eng.csv')`.
- To reproduce the experiments:
	- Run the preprocessing and EDA sections to validate data parsing and missing-value handling.
	- Configure model hyperparameters in the grid-search cells (`p_values`, `d_values`, `q_values`, etc.).
	- Use the `predict_pipeline` function to run ARIMA/SARIMA/SARIMAX/Prophet experiments and evaluate with MSE/MAE/MAPE.

Results (summary)
-----------------
- English pages dominate traffic and provide the most reliable forecasts (lowest MAPE). Seasonal patterns are strong (weekly/quarterly peaks).
- Prophet and tuned SARIMAX models produced the best MAPE in the notebook experiments (MAPE observed ~4–6% for top configurations).

Recommendations
---------------
- Prioritize ad spend on English pages for broad reach and predictable ROI.
- Use exogenous variables (campaign flags) where appropriate — SARIMAX and Prophet support regressors.
- For large-scale production forecasts across many pages, consider automated methods like `auto_arima`, Bayesian optimization, or a scalable gradient-boosting approach (e.g., LightGBM/XGBoost with time features).

Notes & Caveats
---------------
- The notebook includes a long-running grid search (joblib parallelization); running it end-to-end can be time-consuming and compute-intensive.
- Model convergence and numeric stability may require adjusting optimizer settings and increasing `maxiter` for SARIMAX.
