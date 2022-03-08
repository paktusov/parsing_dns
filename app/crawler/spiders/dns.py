from typing import Optional
import datetime as dt
import pytz
import scrapy
import re
import pymongo
from scrapy_selenium import SeleniumRequest
from crawler.items import ProductItem
from config import mongo_config


def parse_price(price: str) -> Optional[int]:
    if not price:
        return None
    return int(re.sub(r"\D+", "", price))


class DNSSpider(scrapy.Spider):
    name = "dns"
    page_num = 1

    def start_requests(self):
        client = pymongo.MongoClient(
            mongo_config.uri,
            username=mongo_config.username,
            password=mongo_config.password
        )
        db = client[mongo_config.database]
        city_link_suffix = db['cities'].find_one({"name": self.city})['link_suffix']
        choice_city = f'https://www.dns-shop.ru/ajax/change-city/?city_guid={city_link_suffix}'
        client.close()
        yield SeleniumRequest(url=choice_city, callback=self.first_page)

    def first_page(self, response):
        start_page = 'https://www.dns-shop.ru/catalog/markdown/'
        yield SeleniumRequest(url=start_page, callback=self.parse_result)

    def parse_result(self, response):
        for product in response.css('div.markdown-page__group-title, div.catalog-product'):
            if product.css('div.markdown-page__group-title'):
                category = product.css('div.markdown-page__group-title::text').get()
            else:
                name, *description = product.css('a.catalog-product__name span::text').getall()
                description = description[0].strip("[]") if description else None
                link = response.urljoin(product.css('a.catalog-product__name::attr(href)').get())
                now = dt.datetime.now()

                yield ProductItem(
                    _id=link.strip("/").split("/")[-1],
                    name=name,
                    category=category,
                    description=description,
                    full_price=parse_price(product.css('div.catalog-product__price-old::text').get()),
                    history_price=[(parse_price(product.css('div.catalog-product__price-actual::text').get()), now)],
                    link=link,
                    image=product.css('div.catalog-product__image img::attr(data-src)').get(),
                    last_update=now,
                    last_seen=now,
                    removed=False
                    )

        next_page = response.css('button.pagination-widget__show-more-btn span::text').get()
        if next_page is not None:
            self.page_num += 1
            next_page = f'https://www.dns-shop.ru/catalog/markdown/?p={self.page_num}'
            yield SeleniumRequest(url=next_page, callback=self.parse_result)
