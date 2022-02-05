from itemadapter import ItemAdapter
import logging
import pymongo
from config import mongo_config


class MongoPipeline():

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
            mongo_config.uri,
            username=mongo_config.username,
            password=mongo_config.password
        )
        self.db = self.client[mongo_config.database]
        if hasattr(spider, 'collection_name'):
            self.collection_name = spider.collection_name

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
