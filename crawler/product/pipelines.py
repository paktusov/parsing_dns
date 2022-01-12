# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


#class TutorialPipeline:
#    def process_item(self, item, spider):
#        return item

import logging
import pymongo

class MongoPipeline(object):

    collection_name = 'dns_goods'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        ## initializing spider
        ## opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        ## clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):
        exist = self.db[self.collection_name].find_one({"_id": dict(item)["_id"]})
        if not exist:
            self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
            logging.debug("Item added to MongoDB")
        else:
            if exist["history_price"][-1][0] != item["history_price"][-1][0]:
                exist["history_price"].append(item["history_price"][-1])
                exist["last_update"] = item["last_update"]
                exist["last_seen"] = item["last_seen"]
                self.db[self.collection_name].find_one_and_replace({"_id": dict(item)["_id"]}, exist)
                logging.debug("Item update to MongoDB")
            else:
                exist["last_seen"] = item["last_seen"]
                self.db[self.collection_name].find_one_and_replace({"_id": dict(item)["_id"]}, exist)
                logging.debug("Item duplicates")
        return item
