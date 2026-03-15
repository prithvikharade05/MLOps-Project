# BTC FORECASTING MLOPS PLATFORM - IMPLEMENTATION TODO

## Project Status: 🚀 In Progress

### Phase 1: Project Structure & Dependencies [5/5] ✅
- [x] Step 1.1: Create root `btc_forecasting/` directory structure (backend subdirs, frontend, infra)
- [x] Step 1.2: Backend `requirements.txt` with all Python deps
- [x] Step 1.3: Frontend `package.json`, Tailwind config, globals.css
- [ ] Step 1.4: `.env.example` and `Makefile`
- [x] Step 1.5: Dockerfiles and `docker-compose.yml` skeleton

### Phase 2: Backend Core [10/12]
- [x] Step 2.1: DB setup (`database/db.py`, `models.py`)
- [x] Step 2.2: Config and utils (`utils/config.py`)
- [x] Step 2.3: Data ingestion (`ingestion/binance_collector.py`, scheduler)
- [x] Step 2.4: Feature engineering (`features/*.py`)
- [x] Step 2.5: Models (`models/*.py`)
- [x] Step 2.6: Model registry MLflow (`model_registry.py`)
- [x] Step 2.7: Monitoring/drift (`monitoring/*.py`)
- [x] Step 2.8: Celery setup (`tasks/celery_app.py`, `pipelines.py`)
- [ ] Step 2.9: FastAPI app (`api/app.py`)
- [x] Step 2.10: API routers (predict, training, monitoring)
- [x] Step 2.11: Schemas (`schemas/*.py`)
- [x] Step 2.12: Backend tests

### Phase 3: Frontend Dashboard [2/12]
- [x] Step 3.1: Next.js layout and globals
- [ ] Step 3.2: UI components (FuturisticCard, NeonButton, GlassPanel)
- [x] Step 3.3: Charts components (PriceChart, MetricsChart)
- [ ] Step 3.4: Widgets (PredictionMeter, StatusIndicator)
- [ ] Step 3.5: Pages: Overview
- [ ] Step 3.6: Pages: Performance
- [ ] Step 3.7: Pages: Monitoring
- [ ] Step 3.8: Pages: Predictions
- [ ] Step 3.9: Pages: Experiments
- [ ] Step 3.10: WebSocket client for real-time
- [ ] Step 3.11: 3D particles background (Three.js)
- [ ] Step 3.12: Frontend tests

### Phase 4: Integration & Deployment [0/6]
- [ ] Step 4.1: Complete Docker Compose (all services)
- [ ] Step 4.2: Nginx config
- [ ] Step 4.3: DB migrations script
- [ ] Step 4.4: Init scripts (MLflow, first ingest)
- [ ] Step 4.5: Full local test (`docker compose up`)
- [ ] Step 4.6: Production hardening (env vars, secrets)

### Phase 5: Advanced Features & Polish [0/5]
- [ ] Step 5.1: Real-time WebSockets in FastAPI
- [ ] Step 5.2: MLflow UI integration in frontend
- [ ] Step 5.3: Auto-scheduling (Celery Beat)
- [ ] Step 5.4: E2E tests and monitoring
- [ ] Step 5.5: Documentation (README.md)

**Next Action: Phase 2 Step 2.9 - FastAPI app**

