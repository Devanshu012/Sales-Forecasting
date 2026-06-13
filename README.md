# Sales Forecasting

An end-to-end machine learning project that predicts daily store sales based on store parameters. The project includes data analysis, model training with MLflow tracking, a FastAPI backend, and a Streamlit frontend — deployed separately on Render and Streamlit Cloud.

---

## Live Demo

| Service | URL |
|---|---|
| Frontend (Streamlit) | _Add your Streamlit Cloud URL here_ |
| Backend API (FastAPI) | _Add your Render URL here_ |
| API Docs | `<your-render-url>/docs` |

---

## Project Structure

```
sales_forecasting/
│
├── backend/                        # FastAPI app — deployed on Render
│   ├── main.py                     # API entry point with /predict endpoint
│   ├── Procfile                    # Render startup command
│   ├── requirements.txt            # Backend dependencies
│   ├── src/
│   │   └── preprocessing.py        # Custom sklearn transformer classes
│   └── models/
│       ├── xgboost_model.pkl       # Trained XGBoost model
│       └── preprocessing_pipeline.pkl
│
├── frontend/                       # Streamlit app — deployed on Streamlit Cloud
│   ├── app.py                      # UI with form inputs and API integration
│   └── requirements.txt            # Frontend dependencies
│
├── notebooks/                      # Jupyter notebooks (development only)
│   ├── 01_EDA.ipynb                # Exploratory data analysis
│   ├── 02_preprocessing.ipynb      # Feature engineering & pipeline building
│   ├── 03_modeling.ipynb           # Model training & MLflow logging
│   └── 04_prediction.ipynb         # Generating predictions on test data
│
├── data/
│   ├── raw/                        # Original dataset (not tracked in git)
│   ├── processed/                  # Preprocessed data (not tracked in git)
│   └── predicted/                  # Model output (not tracked in git)
│
├── src/                            # Shared utilities for notebooks
│   ├── data_loader.py
│   ├── preprocessing.py
│   └── logger.py
│
├── requirements.txt                # Full dev dependencies (notebooks + training)
├── .gitignore
└── README.md
```

---

## Model Performance

Three models were trained and tracked with MLflow:

| Model | Test R² | RMSE |
|---|---|---|
| Decision Tree | 0.9209 | 1081.86 |
| XGBoost | 0.9168 | 1109.95 |
| Random Forest | 0.8888 | 1283.12 |

**XGBoost** was selected for deployment — best balance of accuracy and model size (4.7 MB vs 1.2 GB for Random Forest).

---

## Tech Stack

| Layer | Technology |
|---|---|
| Data Analysis | Pandas, Matplotlib, Seaborn, Plotly |
| ML Training | Scikit-learn, XGBoost |
| Experiment Tracking | MLflow |
| Backend API | FastAPI, Uvicorn |
| Frontend UI | Streamlit |
| Backend Deployment | Render |
| Frontend Deployment | Streamlit Cloud |

---

## API Reference

### `GET /`
Health check.

**Response:**
```json
{ "message": "Sales Forecast API Running" }
```

### `POST /predict`
Predicts daily sales for a store.

**Request body:**
```json
{
  "Store": 1,
  "DayOfWeek": 5,
  "Date": "2015-07-31",
  "Open": 1,
  "Promo": 1,
  "StateHoliday": "0",
  "SchoolHoliday": 1,
  "StoreType": "c",
  "Assortment": "a",
  "CompetitionDistance": 1270.0,
  "CompetitionOpenSinceMonth": 9.0,
  "CompetitionOpenSinceYear": 2008.0,
  "Promo2": 0,
  "Promo2SinceWeek": null,
  "Promo2SinceYear": null,
  "PromoInterval": null
}
```

**Response:**
```json
{ "predicted_sales": 5263.42 }
```

---

## Running Locally

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/sales-forecasting.git
cd sales_forecasting
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Start the backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
API will be available at `http://127.0.0.1:8000`
Interactive docs at `http://127.0.0.1:8000/docs`

### 4. Start the frontend (new terminal)
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```
UI will open at `http://localhost:8501`

---

## Deployment

### Backend → Render

1. Push code to GitHub
2. Go to [render.com](https://render.com) → **New → Web Service**
3. Connect your GitHub repository
4. Set the following:

| Setting | Value |
|---|---|
| Root Directory | `backend` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

5. Click **Deploy** — Render will give you a URL like `https://your-app-name.onrender.com`

### Frontend → Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
2. Connect your GitHub repository
3. Set **Main file path** to `frontend/app.py`
4. Go to **Settings → Secrets** and add:

```toml
BACKEND_URL = "https://your-app-name.onrender.com"
```

5. Click **Deploy**

---

## Environment Variables

| Variable | Service | Description |
|---|---|---|
| `BACKEND_URL` | Frontend | Full URL of the deployed Render backend |
| `PORT` | Backend | Automatically set by Render — do not set manually |

---

## Notebooks

Run notebooks in order for full reproducibility:

| Notebook | Description |
|---|---|
| `01_EDA.ipynb` | Explores distributions, missing values, outliers, and sales patterns |
| `02_preprocessing.ipynb` | Builds the sklearn preprocessing pipeline and saves it |
| `03_modeling.ipynb` | Trains Decision Tree, Random Forest, XGBoost with MLflow tracking |
| `04_prediction.ipynb` | Generates predictions on the test set |

To view MLflow experiment results, run from the project root:
```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```
Then open `http://127.0.0.1:5000`

---

## Dataset

This project uses the [Rossmann Store Sales](https://www.kaggle.com/competitions/rossmann-store-sales) dataset from Kaggle.

The raw data files are not included in this repository. Download them from Kaggle and place them in `data/raw/`:
- `train.csv`
- `test.csv`
- `store.csv`
- `sample_submission.csv`
