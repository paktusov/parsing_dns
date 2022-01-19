import scrapy


class ProductItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    full_price = scrapy.Field()
    history_price = scrapy.Field()
    link = scrapy.Field()
    image = scrapy.Field()
    last_update = scrapy.Field()
    last_seen = scrapy.Field()
    remote = scrapy.Field()
