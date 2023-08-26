#!/bin/bash
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000
#gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000