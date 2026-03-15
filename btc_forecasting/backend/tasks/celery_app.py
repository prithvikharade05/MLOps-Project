from celery import Celery
from utils.config import settings
import os

# Set default config
os.environ.setdefault('CELERY_CONFIG_MODULE', 'config')

app = Celery(
    'btc_forecasting',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        'tasks.pipelines',
        'ingestion.scheduler',
    ]
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_routes={
        'ingestion.scheduler.ingest_data': {'queue': 'data'},
        'tasks.pipelines.create_features': {'queue': 'features'},
        'tasks.pipelines.train_models': {'queue': 'training'},
        'tasks.pipelines.run_drift_check': {'queue': 'monitoring'},
    },
    task_default_queue='default',
    worker_prefetch_multiplier=1,
    worker_concurrency=1,  # One task at a time for data pipeline
)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

