# Phishing Email Detector

## Problem statement
Phishing emails are a high-impact security risk. This project provides a production-minded pipeline to train and deploy a phishing email classifier with a professional web dashboard for explainable predictions.

## Dataset source
Kaggle phishing email dataset: https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset

The training script accepts a configurable path and normalizes common column names (text/body/email + label/is_phishing/target).

## Architecture overview
- Backend: FastAPI service exposing a prediction API with model loading, validation, and explainability.
- ML pipeline: data ingestion, cleaning, feature engineering, training, evaluation, and model export.
- Frontend: Next.js dashboard for analysis, results, and local history.

## Folder structure
- backend/app/api: HTTP routes
- backend/app/services: inference and feature engineering
- backend/app/schemas: request/response validation
- backend/scripts: training pipeline
- frontend/features: detector feature module
- frontend/shared: UI components, hooks, and API client

## Data pipeline (textual diagram)
Ingestion -> Cleaning -> Feature extraction (TF-IDF + engineered features) -> Train/test split -> Train models -> Evaluate -> Select best -> Export

## Model comparison results
The training script outputs metrics for Logistic Regression and Random Forest, then selects the best by F1 score.

## API contract
POST /api/predict
Request JSON:
{
	"body": "...",
	"headers": "..."
}
Response JSON:
{
	"prediction": "phishing",
	"confidence": 0.92,
	"risk_level": "High",
	"explanation": {
		"reasons": ["..."],
		"top_features": [{"feature": "", "contribution": 0.1}],
		"suspicious_terms": ["urgent"],
		"stats": {"phishing_score": 0.92}
	}
}

## Explainability
- Top contributing features for linear models.
- Suspicious term highlighting for UI.
- Optional SHAP hooks for tree models.

## Security considerations
- Input validation with Pydantic and Zod.
- Minimal error leakage in API responses.
- Clear separation of training and inference assets.

## Performance considerations
- Joblib model loading with caching on startup.
- Vectorized feature extraction.

## Project structure
- backend/: FastAPI service, ML pipeline, tests
- frontend/: Next.js dashboard, components, tests

## Dataset Setup

**Option 1: Kaggle API (Recommended)**

1. Install Kaggle API:
   ```bash
   pip install kagglehub
   ```

2. Authenticate with Kaggle:
   - Go to https://www.kaggle.com/settings/account
   - Create API token (downloads kaggle.json)
   - Place kaggle.json at:
     - Windows: `C:\Users\<username>\.kaggle\kaggle.json`
     - Linux/Mac: `~/.kaggle/kaggle.json`

3. Run download script:
   ```bash
   python download_dataset.py
   ```

**Option 2: Manual Download**

1. Download from https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset
2. Extract CSV to `backend/data/phishing_emails.csv`

## Local development
1) Backend
- Create a virtual environment
- Install deps from backend/requirements.txt
- Download dataset (see Dataset Setup above)
- Train a model: `python backend/scripts/train.py`
- Start API: `uvicorn app.main:app --reload --app-dir backend`

2) Frontend
- Install deps from frontend/package.json
- Start dev server: npm run dev -- --hostname 0.0.0.0

## Model evaluation notes
Update this section after training with the selected dataset.
- Accuracy, Precision, Recall, F1, ROC-AUC
- Confusion matrix

## Future improvements
- Rate limiting and auth
- Email header parser and .eml uploads
- Model versioning and registry
- SHAP explanations in UI charts
