# appstore_review/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appstore_review.settings')
app = Celery('appstore_review')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()