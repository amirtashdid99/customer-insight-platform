#!/usr/bin/env python
"""
Celery Worker Entry Point

Start this worker with:
    celery -A worker.celery_app worker --loglevel=info
"""
from app.core.celery_app import celery_app

# Import tasks to register them
from app.tasks import run_analysis_task

if __name__ == '__main__':
    celery_app.start()
