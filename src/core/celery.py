# celery.py
import os
from celery import Celery

# Django 설정을 로드
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('board')

# Django 설정에서 Celery 설정을 가져옴
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django 앱을 자동으로 찾아서 Celery 작업(task)으로 등록
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
