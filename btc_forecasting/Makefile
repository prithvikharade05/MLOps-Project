.PHONY: up down logs migrate init-mlflow ingest-first train-first

up:
	cd btc_forecasting && docker compose up -d

down:
	cd btc_forecasting && docker compose down

logs:
	cd btc_forecasting && docker compose logs -f

migrate-db:
	docker compose exec backend alembic upgrade head

init-mlflow:
	docker compose exec backend mlflow db init -b sqlite:///mlflow.db

ingest-first:
	docker compose exec backend celery -A tasks.celery_app worker --loglevel=info &
	docker compose exec backend python -c "from tasks.pipelines import ingest_data; ingest_data.delay()"

train-first:
	docker compose exec backend python backend/models/train_linear_regression.py

