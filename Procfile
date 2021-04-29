release: python manage.py migrate
worker: celery -A planeks.celery worker -B --loglevel=info
web: gunicorn planeks.wsgi