from celery import Celery
from celery.schedules import crontab
import crawler.settings
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.spiders.dns import DNSSpider
from config import celery_config
from mongo import db


def init_schedule_for_cities():
    cities = list(db['cities'].find())
    for city in cities:
        app.conf.beat_schedule[f'parsing_{city["name"]}'] = {
            'task': 'crawler.tasks.start_parsing',
            'schedule': crontab(**city['schedule']),
            'args': (city['name'],)
        }


app = Celery('tasks', broker=celery_config.broker)
app.conf.update(
    worker_max_tasks_per_child=celery_config.worker_max_tasks_per_child,
    broker_pool_limit=celery_config.broker_pool_limit,
    timezone=celery_config.timezone,
)
app.conf.beat_schedule = dict()
init_schedule_for_cities()


@app.task
def start_parsing(city):
    process = CrawlerProcess(get_project_settings())
    process.crawl(DNSSpider, city=city)
    process.start()
