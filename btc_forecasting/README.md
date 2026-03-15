# BTC Forecasting MLOps Platform

Futuristic institutional-grade Bitcoin forecasting system with full MLOps pipeline.

## Quick Start
```bash
docker compose up -d
make migrate-db
make init-mlflow
make ingest-first
```

Access:
- Dashboard: http://localhost
- API: http://localhost/api/docs
- MLflow: http://localhost:5000

