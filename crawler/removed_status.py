import datetime as dt
import pymongo
import scrapy
import product.settings
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from product.spiders.product_spider import ProductSpider

now = dt.datetime.now().isoformat()

settings = get_project_settings()
crawler = CrawlerProcess(settings=settings)
crawler.crawl(ProductSpider)
crawler.start()


client = pymongo.MongoClient('mongodb://localhost:2717')
db = client['parsing_dns']
collection_name = 'dns_goods'

removed = db[collection_name].update_many({'last_seen': {'$lt': now}}, {'$set': {'removed': True}})
print(f'Has been removed: {removed.modified_count}')
