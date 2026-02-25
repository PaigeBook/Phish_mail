# Testing Guide

## Running Tests

### Backend Tests

**Install test dependencies:**
```bash
cd backend
.venv\Scripts\python.exe -m pip install pytest pytest-cov
```

**Run all tests:**
```bash
.venv\Scripts\python.exe -m pytest tests/ -v
```

**Run with coverage:**
```bash
.venv\Scripts\python.exe -m pytest tests/ -v --cov=app --cov-report=html
```

**Run specific test file:**
```bash
.venv\Scripts\python.exe -m pytest tests/test_features.py -v
```

### Frontend Tests

**Run frontend tests:**
```bash
cd frontend
npm run test
```

## Test Coverage

### Backend Tests

- **test_features.py**: Feature extraction pipeline
  - Shape validation
  - Suspicious keyword detection
  - URL and IP-URL detection
  - Special character counting

- **test_services.py**: ML services
  - Single email prediction
  - Batch prediction
  - Health check
  - Model metadata loading

- **test_api_endpoints.py**: API endpoints
  - Health endpoint
  - Single prediction endpoint
  - Batch prediction endpoint
  - Input validation
  - Error handling

### Frontend Tests

- **DetectorPage.test.tsx**: Main UI component
  - Form submission
  - Results display
  - History tracking
  - Error states

## CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/ci.yml`):

- **Backend Tests**: Runs pytest with coverage on Python 3.11
- **Backend Lint**: Black and Ruff checks
- **Frontend Tests**: ESLint and Vitest
- **Docker Build**: Builds backend and frontend images

Workflows trigger on: `push` to main/develop, `pull_request` to main/develop

## Code Quality Standards

- **Backend**: Black (formatting), Ruff (linting), Pytest (testing)
- **Frontend**: Prettier (formatting), ESLint (linting), Vitest (testing)

## Local Testing Before Push

```bash
# Backend
cd backend
.venv\Scripts\python.exe -m pytest tests/ -v
.venv\Scripts\python.exe -m black --check .
.venv\Scripts\python.exe -m ruff check .

# Frontend
cd frontend
npm run lint
npm run test
```
