# Phishing Email Detector - Portfolio Highlights

## Executive Summary

This is a **production-quality ML project** demonstrating:
- Clean software architecture with proper separation of concerns
- ML pipeline best practices (data → features → train → evaluate → export)
- Professional backend API design with multiple enriched endpoints
- Modern frontend dashboard with real-time predictions
- Comprehensive testing, CI/CD, and observability

**Live App** (when running): http://localhost:3000  
**API Docs**: http://localhost:8000/docs

---

## Key Architectural Decisions

### 1. **Multi-Endpoint Strategy** (Portfolio Signal: Production Thinking)
- `GET /api/health` - Monitor model state without predictions
- `POST /api/predict` - Single email analysis with explainability
- `POST /api/predict-batch` - Process up to 1000 emails per request

**Why This Matters**: Shows understanding of real-world requirements (not just one endpoint). Production systems need monitoring, single analysis, and bulk capabilities.

### 2. **Structured Logging & Request Tracing** (Portfolio Signal: Observability)
- Request/response middleware logs all interactions
- Unique request IDs for debugging
- Timing information for performance analysis
- Error stack traces with context

**Why This Matters**: Demonstrates DevOps/SRE thinking. Hiring managers look for this in production engineers.

### 3. **Feature Engineering Modularity** (Portfolio Signal: ML Rigor)
```python
# Clean transformer interface (Scikit-learn standard)
class EngineeredFeatures(BaseEstimator, TransformerMixin):
    - Follows ML conventions
    - No data leakage
    - Reusable in pipelines
```

**Why This Matters**: Shows deep ML fundamentals. Not just model training, but proper feature engineering practices.

### 4. **Comprehensive Test Coverage** (Portfolio Signal: Quality Assurance)
- **Backend**: Feature extraction, model inference, API endpoints, error cases
- **Frontend**: Component rendering, interactions, error states
- **CI/CD**: Automated testing on every commit/PR

**Why This Matters**: Professional projects have tests. Shows confidence in code quality.

### 5. **Model Metadata in Responses** (Portfolio Signal: Production ML)
```json
{
  "status": "ok",
  "model_loaded": true,
  "model_name": "random_forest",
  "trained_at": "2026-02-25T18:12:18.751247",
  "accuracy": 0.9938705146213765
}
```

**Why This Matters**: Real ML systems track model versions and performance. This shows MLOps awareness.

---

## Technical Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Backend ML** | Python + FastAPI | Industry standard for ML APIs |
| **Data Processing** | Pandas + NumPy | Vectorized, efficient operations |
| **Feature Engineering** | Scikit-learn pipelines | Proper separation, no data leakage |
| **Model Training** | Logistic Regression + Random Forest | Baseline + advanced, show understanding of tradeoffs |
| **Model Persistence** | Joblib | Standard ML model serialization |
| **Frontend** | Next.js + TypeScript + TailwindCSS | Modern React, type-safe, professional UI |
| **State Management** | React Query + Zod | Industry best practices |
| **Testing** | Pytest + Vitest | Comprehensive coverage both ends |
| **Deployment** | Docker (optional) | Production-ready containerization |
| **CI/CD** | GitHub Actions | Automated quality gates |

---

## Project Structure (Clean Architecture)

```
backend/
├── app/
│   ├── api/              # HTTP route handlers
│   ├── services/         # Business logic (inference, health, batch)
│   ├── middleware/       # Logging, error handling
│   ├── schemas/          # Request/response validation (Pydantic)
│   └── models/           # Model artifacts (trained models)
│
├── scripts/
│   └── train.py          # Complete training pipeline
│
└── tests/
    ├── test_features.py     # Feature extraction tests
    ├── test_services.py     # ML service tests
    ├── test_api_endpoints.py # Integration tests
    └── test_predict.py      # Prediction tests

frontend/
├── app/                  # App Router pages
├── features/detector/    # Feature module
├── shared/
│   ├── components/       # Reusable UI components
│   ├── hooks/           # Custom React hooks
│   └── lib/             # Utilities, API client
└── tests/               # Component tests
```

**Signal**: No monolithic files. Clear separation. Scalable structure.

---

## Model Performance

| Metric | Logistic Regression | Random Forest |
|--------|-------------------|----------------|
| Accuracy | 99.32% | **99.39%** ✓ |
| Precision | 99.16% | **99.43%** ✓ |
| Recall | 99.63% | **99.47%** |
| F1 Score | 99.39% | **99.45%** ✓ |
| ROC-AUC | 99.94% | **99.97%** ✓ |

**Selected**: Random Forest (best F1 and ROC-AUC)

---

## Testing Strategy

### Backend (pytest)
```bash
pytest backend/tests -v --cov=app
```

**Coverage**:
- Feature extraction pipeline (6 tests)
- Model inference and batch processing (5 tests)
- API endpoints and validation (6 tests)

### Frontend (Vitest)
```bash
cd frontend && npm run test
```

**Coverage**:
- Component rendering
- User interactions
- Error states

### CI/CD (GitHub Actions)
```yaml
- Backend tests with coverage reporting
- Code linting (Black + Ruff)
- Frontend tests + linting
- Docker builds validation
```

---

## API Examples

### Health Check
```bash
curl http://localhost:8000/api/health
```
Returns model status, accuracy, last trained date.

### Single Prediction
```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "body": "URGENT: Verify your account now",
    "headers": null
  }'
```

### Batch Prediction
```bash
curl -X POST http://localhost:8000/api/predict-batch \
  -H "Content-Type: application/json" \
  -d '{
    "emails": [
      {"body": "text1", "headers": null},
      {"body": "text2", "headers": null}
    ]
  }'
```

---

## Deployment Ready

- **Docker support** for both backend and frontend
- **Environment configuration** via .env files
- **Graceful error handling** with structured logging
- **Request validation** at all endpoints (Pydantic/Zod)
- **CORS configured** for cross-origin requests

---

## What Hiring Managers Notice

✅ **Clean Code**: Proper module organization, naming conventions, no copy-paste  
✅ **ML Rigor**: Feature engineering best practices, proper train/test separation  
✅ **Production Thinking**: Logging, monitoring, batch processing, health checks  
✅ **Testing**: Comprehensive coverage, CI/CD pipeline  
✅ **Documentation**: README, ARCHITECTURE.md, TESTING.md, inline comments  
✅ **Dashboard Design**: Professional UI with security-focused aesthetics  
✅ **Git History**: Will show iterative development (commits, PRs)  

---

## Getting Started

1. **Install dependencies**:
   ```bash
   cd backend && pip install -r requirements.txt
   cd frontend && npm install
   ```

2. **Download dataset**:
   ```bash
   python download_dataset.py  # Requires Kaggle credentials
   ```

3. **Train model**:
   ```bash
   cd backend && python scripts/train.py
   ```

4. **Run local**:
   ```bash
   # Backend
   cd backend && uvicorn app.main:app --reload --port 8000
   
   # Frontend (new terminal)
   cd frontend && npm run dev
   ```

5. **Run tests**:
   ```bash
   # Backend
   cd backend && pytest tests/ -v
   
   # Frontend
   cd frontend && npm run test
   ```

Visit http://localhost:3000

---

## Recommended Demo Flow

1. Show **healthy model** via `/api/health`
2. Analyze a **phishing email** - show high confidence + flags
3. Analyze **legitimate email** - show low risk
4. Show **batch prediction** with 10 emails
5. Mention CI/CD pipeline + test coverage
6. Walk through **architecture decisions** in ARCHITECTURE.md

---

## Next Steps (Future Enhancements)

- [ ] Rate limiting with Redis
- [ ] JWT authentication
- [ ] Email header parser (.eml support)
- [ ] Model versioning/registry
- [ ] Prediction history database
- [ ] Admin dashboard with metrics
- [ ] Kubernetes deployment manifests
- [ ] Performance benchmarking
