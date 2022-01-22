import datetime as dt
import pymongo
import scrapy
import os
from dotenv import load_dotenv
import crawler.settings
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.spiders.dns import DNSSpider
load_dotenv()

now = dt.datetime.now().isoformat()

settings = get_project_settings()
crawler = CrawlerProcess(settings=settings)
crawler.crawl(DNSSpider)
crawler.start()

mongo_uri = os.getenv('MONGODB_URI')
mongo_username = os.getenv('MONGODB_USERNAME')
mongo_password = os.getenv('MONGODB_PASSWORD')
client = pymongo.MongoClient(
    mongo_uri,
    username=mongo_username,
    password=mongo_password
)
db = client['parsing_dns']
collection_name = 'dns_goods'

removed = db[collection_name].update_many({'last_seen': {'$lt': now}}, {'$set': {'removed': True}})
print(f'Has been removed: {removed.modified_count}')
