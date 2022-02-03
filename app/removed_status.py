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
load_dotenv()


def send_sms(sms_text):
    account_sid = os.getenv('twilio_account_sid')
    auth_token = os.getenv('twilio_auth_token')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=os.getenv('to'),
        from_=os.getenv('from_'),
        body=sms_text)
    return message.sid


def sendmessage_to_telegram(text):
    token = os.getenv('telegram_token')
    bot = telebot.TeleBot(token)
    chatid = os.getenv('id')
    bot.send_message(chatid, text=text)


def sendphoto_to_telegram(product):
    token = os.getenv('telegram_token')
    bot = telebot.TeleBot(token)
    chatid = os.getenv('id')
    last_price = product['history_price'][-1][0]
    last_update_fmt = dt.datetime.fromisoformat(product['last_update']).strftime("%Y.%m.%d %H:%M")
    caption = '<a href="{}">{}</a>\n\n{}\n\n{} р. | {} р.\n\n{}'
    format_caption = caption.format(product['link'],
                             product['name'],
                             product['description'],
                             last_price,
                             product['full_price'],
                             last_update_fmt)
    bot.send_photo(chatid, photo=product['image'], caption=format_caption, parse_mode='HTML')


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

updated = list(db[collection_name].find({'last_update': {'$gt': now}}))
if updated:
#    send_sms("Появились новые товары!")
    for product in updated:
        sendphoto_to_telegram(product)
