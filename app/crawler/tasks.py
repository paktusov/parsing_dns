from celery import Celery
from celery.schedules import crontab
from update_notification import parsing_city

app = Celery('tasks', broker='redis://redis')
app.conf.timezone = 'Asia/Yekaterinburg'

app.conf.beat_schedule = {
    'parsing_chelyabinsk_every_20_minutes': {
        'task': 'crawler.tasks.start_parsing',
        'schedule': crontab(minute='*/1'),
        'args': ('chelyabinsk',)
    },
    'parsing_ekaterinburg_once_a_day': {
        'task': 'crawler.tasks.start_parsing',
        'schedule': crontab(minute=0, hour=2),
        'args': ('ekaterinburg',)
    }
}

@app.task
def start_parsing(city):
    parsing_city(city)
