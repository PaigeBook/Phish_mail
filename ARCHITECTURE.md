# Architecture Decision Records

## ADR-001: Batch Prediction Endpoint

**Status**: Implemented  
**Date**: 2026-02-25

### Context
Single predictions are useful, but real-world phishing detection often processes many emails at once.

### Decision
- Added `/api/predict-batch` endpoint with max 1000 emails per request
- Returns batch_id for tracking and status tracking
- Individual prediction errors don't fail the batch (graceful degradation)

### Rationale
Portfolio signal: shows production thinking, handles scale, provides flexibility for different usage patterns.

---

## ADR-002: Health Check with Metadata

**Status**: Implemented  
**Date**: 2026-02-25

### Context
Monitoring and debugging require insight into model state without invoking predictions.

### Decision
- Enhanced `/api/health` endpoint returns model metadata (name, training time, accuracy)
- Status field indicates if model is loaded
- Includes version for API compatibility tracking

### Rationale
Shows MLOps awareness. Hiring managers recognize this as production best practice.

---

## ADR-003: Structured Logging & Middleware

**Status**: Implemented  
**Date**: 2026-02-25

### Context
Production systems need observability. Log aggregation systems require consistent structure.

### Decision
- Request/response logging middleware with timing
- Structured logging with request IDs
- Error tracking with full stack traces
- All logs include timestamp, level, context

### Rationale
Demonstrates maturity in deployment thinking. Shows familiarity with monitoring/debugging production systems.

---

## ADR-004: Feature Engineering Separation

**Status**: Implemented  
**Date**: 2026-02-25

### Context
ML pipelines need clear separation between training (transforming features) and inference (applying transformations).

### Decision
- EngineeredFeatures class implements Scikit-learn's transformer interface
- Features computed on demand during prediction
- No data leakage between train/test

### Rationale
Shows ML fundamentals. Hiring managers recognize proper pipeline design.

---

## ADR-005: Risk Level Thresholds

**Status**: Implemented  
**Date**: 2026-02-25

### Decision
- Low: phishing_score < 0.4
- Medium: 0.4 ≤ phishing_score < 0.7
- High: phishing_score ≥ 0.7

### Rationale
Balanced between false positives and false negatives for security use case.

---

## ADR-006: Test Coverage Strategy

**Status**: Implemented  
**Date**: 2026-02-25

### Decision
- Unit tests for feature extraction, services, and utilities
- Integration tests for API endpoints
- Fixtures for mock models to avoid test dependencies
- Frontend tests for component rendering and interactions

### Rationale
Comprehensive coverage shows quality consciousness and testing maturity.
