import os

# settings: https://docs.gunicorn.org/en/stable/settings.html
max_requests = 1000
max_requests_jitter = 100
bind = "0.0.0.0:8080"
workers = 2
worker_class = "uvicorn.workers.UvicornWorker"
reload = True
if os.environ.get("RELOAD"):
    reload = os.environ["RELOAD"]
