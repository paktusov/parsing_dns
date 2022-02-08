from typing import Optional
import datetime as dt
import pytz
import scrapy
import re
from scrapy_selenium import SeleniumRequest
from crawler.items import ProductItem


def parse_price(price: str) -> Optional[int]:
    if not price:
        return None
    return int(re.sub(r"\D+", "", price))


cities = {'chelyabinsk': 'b464725e-819d-11de-b404-00151716f9f5',
          'ekaterinburg': '83878977-f329-11dd-9648-00151716f9f5',
          }


class DNSSpider(scrapy.Spider):
    name = "dns"
    i = 1

    def start_requests(self):
        choice_city = f'https://www.dns-shop.ru/ajax/change-city/?city_guid={cities[self.city]}'
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
                now = dt.datetime.now().isoformat()

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
            self.i += 1
            next_page = f'https://www.dns-shop.ru/catalog/markdown/?p={self.i}'
            yield SeleniumRequest(url=next_page, callback=self.parse_result)
