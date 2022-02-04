import datetime as dt
import pymongo
import scrapy
import os
import telebot
from dotenv import load_dotenv
from twilio.rest import Client
import crawler.settings
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.spiders.dns import DNSSpider
from settings import MongoDBSettings, TelegramNotificationSettings, TwilioSMSNotificationSettings


def send_sms(sms_text, settings):
    account_sid = settings.twilio_account_sid
    auth_token = settings.twilio_auth_token
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=settings.to,
        from_=settings.from_,
        body=sms_text
    )
    return message.sid


def send_photo_to_telegram(product, settings):
    token = settings.telegram_token
    bot = telebot.TeleBot(token)
    chatid = settings.id
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
    bot.send_photo(chatid, photo=product['image'], caption=format_caption, parse_mode='HTML')


if __name__ == "__main__":
    now = dt.datetime.now().isoformat()

    # start parsing
    crawler_settings = get_project_settings()
    crawler = CrawlerProcess(settings=crawler_settings)
    crawler.crawl(DNSSpider)
    crawler.start()

    # connection with DB
    mongo_settings = MongoDBSettings()
    mongo_uri = mongo_settings.MONGODB_URI
    mongo_username = mongo_settings.MONGODB_USERNAME
    mongo_password = mongo_settings.MONGODB_PASSWORD
    client = pymongo.MongoClient(
        mongo_uri,
        username=mongo_username,
        password=mongo_password
    )
    db = client['parsing_dns']
    collection_name = 'dns_goods'

    # update removed status in DB
    removed = db[collection_name].update_many({'last_seen': {'$lt': now}}, {'$set': {'removed': True}})
    print(f'Has been removed: {removed.modified_count}')

    # notification
    sms_settings = TwilioSMSNotificationSettings()
    tlg_settings = NotificationSettings()
    updated = list(db[collection_name].find({'last_update': {'$gt': now}}))
    if updated:
    #    send_sms("Появились новые товары!", sms_settings)
        for product in updated:
            send_photo_to_telegram(product, tlg_settings)
