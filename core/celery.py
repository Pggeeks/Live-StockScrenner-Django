from __future__ import absolute_import,unicode_literals
from argparse import Namespace
import os
from datetime import timezone
from celery import Celery
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE','core.settings')
app = Celery('stockapp')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')
app.config_from_object(settings,namespace='CELERY')
app.conf.beat_schedule ={
    # 'every-1-seconds':{
    #     'task':'stockapp.tasks.update_data',
    #     'schedule': 1,
    #     'args':('infy',),
    # },
}

app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    print(self.request)