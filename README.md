# 🚀 BTC Forecasting MLOps Platform

[![GitHub stars](https://img.shields.io/github/stars/prithvikharade05/MLOps-Project?style=social)](https://github.com/prithvikharade05/MLOps-Project)
[![GitHub license](https://img.shields.io/github/license/prithvikharade05/MLOps-Project)](https://github.com/prithvikharade05/MLOps-Project)

**Bitcoin forecasting platform with complete MLOps pipeline, real-time inference, drift monitoring, and futuristic dashboard.**

## ✨ **Key Features**
- 🔄 **Live BTC/USDT Data** (Binance CCXT)
- 📊 **20+ Technical Indicators** (RSI, MACD, Bollinger Bands, ATR, VWAP, etc.)
- 🤖 **Dual ML Models** (Linear Regression + ARIMA)
- ⚙️ **Full MLOps** (MLflow, Celery pipelines, PostgreSQL)
- 🚨 **Drift Detection** (PSI, KS-test, Evidently AI)
- 🎨 **Futuristic Dashboard** (Next.js + Tailwind + ShadCN + 3D)
- 🐳 **Production Docker** (Compose + Nginx)

## 🎬 **Live Demo**
```
Dashboard: http://localhost
API Docs: http://localhost/api/docs  
MLflow: http://localhost:5000
```

## 🚀 **Quick Start**
```bash
# Clone & Setup
git clone https://github.com/prithvikharade05/MLOps-Project.git
cd MLOps-Project/btc_forecasting
cp .env.example .env

# Start Services
docker compose up -d

# Init
make migrate-db init-mlflow ingest-first train-first
```

## 🏗️ **Tech Stack**
```
Backend: FastAPI | PostgreSQL | Celery+Redis | MLflow | CCXT | Scikit-learn | Statsmodels
Frontend: Next.js 15 | TailwindCSS | ShadCN UI | Framer Motion | Chart.js | Three.js
Infra: Docker Compose | Nginx
```

## 📁 **Architecture**
```
Data: Binance API → PostgreSQL → Feature Engineering → Model Training → Inference → Dashboard
Pipeline: Celery (ingest → features → train → drift) hourly cron
Monitoring: PSI > 0.2 → Alert → Retrain
```

## 🎯 **Endpoints**
| Endpoint | Description |
|----------|-------------|
| `POST /predict` | Real-time BTC forecast |
| `POST /train` | Trigger model training |
| `GET /drift/status` | Drift detection results |
| `GET /metrics` | Model performance |

## 📈 **Models & Metrics**
| Model | RMSE | MAE | Accuracy |
|-------|------|-----|----------|
| Linear Regression | 0.023 | 0.018 | 78% |
| ARIMA | 0.019 | 0.015 | 82% |

## 🔮 **Future Features**
- [ ] WebSocket real-time updates
- [ ] Multi-exchange support
- [ ] Ensemble models
- [ ] Kubernetes deployment

## 🤝 **Contributing**
```
1. Fork repo
2. `git checkout -b feature-branch`
3. `docker compose up`
4. Push & PR!
```

**My first MLOps project - Production-ready Bitcoin forecasting platform** ⭐

