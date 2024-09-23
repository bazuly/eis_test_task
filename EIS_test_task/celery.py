import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EIS_test_task.settings')

app = Celery('EIS_test_task')
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.update(
    BROKER_URL='redis://redis:6380/0',
    CELERY_RESULT_BACKEND='redis://redis:6380/0',
)

app.autodiscover_tasks()