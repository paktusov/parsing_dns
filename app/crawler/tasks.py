from celery import Celery
from celery.schedules import crontab
from start_parsing import parsing_city
from config import celery_config

app = Celery('tasks', broker=celery_config.broker)
app.conf.update(
    worker_max_tasks_per_child=celery_config.worker_max_tasks_per_child,
    broker_pool_limit=celery_config.broker_pool_limit,
    timezone=celery_config.timezone,
)

app.conf.beat_schedule = {
    'parsing_chelyabinsk_every_20_minutes': {
        'task': 'crawler.tasks.start_parsing',
        'schedule': crontab(minute='*/20'),
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
