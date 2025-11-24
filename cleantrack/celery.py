"""
Celery configuration for CleanTrack
"""
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cleantrack.settings')

app = Celery('cleantrack')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Periodic tasks
app.conf.beat_schedule = {
    'check-overdue-cleanings': {
        'task': 'compliance.tasks.check_overdue_cleanings',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
    'generate-daily-compliance-report': {
        'task': 'compliance.tasks.generate_daily_compliance_report',
        'schedule': crontab(hour=8, minute=0),  # Every day at 8 AM
    },
    'check-subscription-status': {
        'task': 'billing.tasks.check_subscription_status',
        'schedule': crontab(hour=0, minute=0),  # Daily at midnight
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
