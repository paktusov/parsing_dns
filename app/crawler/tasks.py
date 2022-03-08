import pymongo
from celery import Celery
from celery.schedules import crontab
import scrapy
import crawler.settings
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.spiders.dns import DNSSpider
from config import celery_config, mongo_config


def init_schedule_for_cities():
    client = pymongo.MongoClient(
        mongo_config.uri,
        username=mongo_config.username,
        password=mongo_config.password
    )
    db = client[mongo_config.database]
    cities = list(db['cities'].find())
    for city in cities:
        schedule = dict(city['schedule'])
        app.conf.beat_schedule[f'parsing_{city["name"]}'] = {
            'task': 'crawler.tasks.start_parsing',
            'schedule': crontab(minute=schedule['minute'], hour=schedule['hour']),
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
    crawler_settings = get_project_settings()
    crawler = CrawlerProcess(settings=crawler_settings)
    crawler.crawl(DNSSpider, city=city)
    crawler.start()
