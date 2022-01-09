# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
#from scrapy.item import Item, Field
import scrapy
from dataclasses import dataclass


class TutorialItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    full_price = scrapy.Field()
    history_price = scrapy.Field()
    link = scrapy.Field()
    image = scrapy.Field()

