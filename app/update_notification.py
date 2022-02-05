import datetime as dt
import pymongo
import scrapy
import telebot
from twilio.rest import Client
import crawler.settings
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.spiders.dns import DNSSpider
from config import telegram_config, twilio_config, mongo_config


def send_sms(sms_text):
    client = Client(twilio_config.account_sid, twilio_config.auth_token)
    message = client.messages.create(
        to=twilio_config.to,
        from_=twilio_config.from_,
        body=sms_text
    )
    return message.sid


def send_photo_to_telegram(product):
    bot = telebot.TeleBot(telegram_config.token)
    last_price = product['history_price'][-1][0]
    last_update_fmt = dt.datetime.fromisoformat(product['last_update']).strftime("%Y.%m.%d %H:%M")
    caption = '<a href="{}">{}</a>\n\n{}\n\n{} р. | {} р.\n\n{}'
    format_caption = caption.format(product['link'],
                                    product['name'],
                                    product['description'],
                                    last_price,
                                    product['full_price'],
                                    last_update_fmt
                                    )
    bot.send_photo(telegram_config.id, photo=product['image'], caption=format_caption, parse_mode='HTML')


if __name__ == "__main__":
    now = dt.datetime.now().isoformat()

    # start parsing
    crawler_settings = get_project_settings()
    crawler = CrawlerProcess(settings=crawler_settings)
    crawler.crawl(DNSSpider)
    crawler.start()

    # connection with DB
    client = pymongo.MongoClient(
        mongo_config.uri,
        username=mongo_config.username,
        password=mongo_config.password
    )
    db = client[mongo_config.database]
    collection_name = 'chelyabinsk'

    # update removed status in DB
    removed = db[collection_name].update_many({'last_seen': {'$lt': now}}, {'$set': {'removed': True}})
    print(f'Has been removed: {removed.modified_count}')

    # notification
    updated = list(db[collection_name].find({'last_update': {'$gt': now}}))
    if updated:
    #    send_sms("Появились новые товары!")
        for product in updated:
            send_photo_to_telegram(product)
