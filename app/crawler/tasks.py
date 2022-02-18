from celery import Celery
from celery.schedules import crontab
from update_notification import parsing_city

app = Celery('tasks', broker='redis://localhost')
app.conf.timezone = 'Asia/Yekaterinburg'

app.conf.beat_schedule = {
    'parsing_chelyabinsk_every_20_minutes': {
        'task': 'tasks.start_parsing',
        'schedule': crontab(minute='*/5'),
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
    parsing_city(city)

if __name__ == '__main__':
    app.start()