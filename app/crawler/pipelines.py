import datetime as dt
import logging

from itemadapter import ItemAdapter
from mongo import get_db
from utils.notifications import send_photo_to_telegram, send_sms


class MongoPipeline:

    def open_spider(self, spider):
        self.db = get_db()
        self.now_time = dt.datetime.now()
        if hasattr(spider, 'city'):
            self.collection_name = spider.city

    def close_spider(self, spider):
        removed = self.db[self.collection_name].update_many({'last_seen': {'$lt': self.now_time}},
                                                            {'$set': {'removed': True}})
        logging.debug(f'Has been removed: {removed.modified_count}')
        updated = list(self.db[self.collection_name].find({'last_update': {'$gt': self.now_time}}))
        if updated:
            #send_sms("Появились новые товары!")
            for product in updated:
                send_photo_to_telegram(product, spider.city)
        logging.debug(f'Has been updated: {len(updated)}')

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
