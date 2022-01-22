from itemadapter import ItemAdapter
import logging
import pymongo
import os
from dotenv import load_dotenv
load_dotenv()


class MongoPipeline(object):
    collection_name = 'dns_goods'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.mongo_username = os.getenv('MONGODB_USERNAME')
        self.mongo_password = os.getenv('MONGODB_PASSWORD')
        self.client = pymongo.MongoClient(
            self.mongo_uri,
            username=self.mongo_username,
            password=self.mongo_password
        )
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        id = dict(item)["_id"]
        exist = self.db[self.collection_name].find_one({"_id": id})
        if not exist:
            self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
            logging.debug("Item added to MongoDB")
        else:
            if exist["history_price"][-1][0] != item["history_price"][-1][0]:
                exist["history_price"].append(item["history_price"][-1])
                exist["last_update"] = item["last_update"]
                logging.debug("Item update to MongoDB")
            else:
                logging.debug("Item duplicates")
            exist["last_seen"] = item["last_seen"]
            exist["removed"] = False
            self.db[self.collection_name].find_one_and_replace({"_id": id}, exist)
        return item
