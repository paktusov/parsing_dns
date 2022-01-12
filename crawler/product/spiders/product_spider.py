from scrapy_selenium import SeleniumRequest
import scrapy
import re
from typing import Optional
from product.items import ProductItem
import datetime as dt

def parse_price(price: str) -> Optional[int]:
  if not price:
      return None
  return int(re.sub(r"\D+", "", price))

class ProductSpider(scrapy.Spider):
    name = "product"
    i = 1
    def start_requests(self):
        url = f'https://www.dns-shop.ru/catalog/markdown/?p={self.i}'
        yield SeleniumRequest(url=url, callback=self.parse_result, cookies={'city_path': 'chelyabinsk'})


    def parse_result(self, response):
        for product in response.css('div.catalog-product'):

            name, *description = product.css('a.catalog-product__name span::text').getall()
            description = description[0].strip("[]") if description else None
            link = response.urljoin(product.css('a.catalog-product__name::attr(href)').get())

            yield ProductItem(
                _id=product.css('a.catalog-product__name::attr(href)').get().strip("/").split("/")[-1],
                name=name,
                description=description,
                full_price=parse_price(product.css('div.catalog-product__price-old::text').get()),
                history_price=[(parse_price(product.css('div.catalog-product__price-actual::text').get()),
                               (dt.datetime.utcnow() + dt.timedelta(hours=5)).strftime("%D %H:%M"))],
                link=link,
                image=product.css('div.catalog-product__image img::attr(data-src)').get(),
                last_update=(dt.datetime.utcnow() + dt.timedelta(hours=5)).strftime("%D %H:%M"),
                last_seen=(dt.datetime.utcnow() + dt.timedelta(hours=5)).strftime("%D %H:%M"),
            )

        next_page = response.css('button.pagination-widget__show-more-btn span::text').get()
        if next_page is not None:

            self.i += 1
            next_page = f'https://www.dns-shop.ru/catalog/markdown/?p={self.i}'
            yield SeleniumRequest(url=next_page, callback=self.parse_result, cookies={'city_path': 'chelyabinsk'})

