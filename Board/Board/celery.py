import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Board.settings')

app = Celery('Board')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send_all_week_posts_every_monday_8am': {
        'task': 'adboard.tasks.all_week_posts',
        # раньше работало так
        # 'schedule': crontab(hour=5, minute=0, day_of_week='monday'),
        # проверка
        # 'schedule': crontab(hour='20', minute='08', day_of_week='tuesday'),
        'schedule': crontab(hour='20', minute='30', day_of_week='monday'),
        'args': (),
    },
}

# если сейчас 22:20, то -> 19:20