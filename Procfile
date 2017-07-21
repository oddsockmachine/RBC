redis: docker run -p 6379:6379 redis
watcher: PYTHONUNBUFFERED=true python watch_logfiles.py
listener: PYTHONUNBUFFERED=true python file_event_listener.py

# https://honcho.readthedocs.io/en/latest/using_procfiles.html#syntax
# venv/bin/celery worker -A app.celery --loglevel=info --beat --concurrency=20 -n worker1@%h
# venv/bin/celery worker -A app.celery --loglevel=info --concurrency=20 -n worker2@%h
# flower -A app.celery --port=5555
