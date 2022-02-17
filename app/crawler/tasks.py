from celery import Celery
from celery.schedules import crontab
import update_notification

app = Celery('tasks', broker='redis://localhost')
app.conf.timezone = 'Asia/Yekaterinburg'

app.conf.beat_schedule = {
    'parsing_chelyabinsk_every_20_minutes': {
        'task': 'tasks.start_parsing',
        'schedule': crontab(minute='*/20'),
        'args': ('chelyabinsk')
    },
    'parsing_ekaterinburg_once_a_day': {
        'task': 'tasks.start_parsing',
        'schedule': crontab(minute=0, hour=2),
        'args': ('ekaterinburg')
    }
}

@app.task
def start_parsing(city):
    update_notifications(city)

