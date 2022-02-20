from celery import Celery
from celery.schedules import crontab
import scrapy
import crawler.settings
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.spiders.dns import DNSSpider
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
    crawler_settings = get_project_settings()
    crawler = CrawlerProcess(settings=crawler_settings)
    crawler.crawl(DNSSpider, city=city)
    crawler.start()
