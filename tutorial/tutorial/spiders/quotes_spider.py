from scrapy_selenium import SeleniumRequest
import scrapy
import re
from typing import Optional

def parse_price(price: str) -> Optional[int]:
  if not price:
      return None
  return int(re.sub(r"\D+", "", price))

class QuotesSpider(scrapy.Spider):
    name = "markdown"
    i = 1
    def start_requests(self):

        urls = [
            f'https://www.dns-shop.ru/catalog/markdown/?p={self.i}'
        ]
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.parse_result, cookies={'city_path': 'chelyabinsk'})


    def parse_result(self, response):
        for product in response.css('div.catalog-product'):
            name, *description = product.css('a.catalog-product__name span::text').getall()
            description = description[0][1:-1] if description else None
            link = 'https://www.dns-shop.ru' + \
                product.css('a.catalog-product__name::attr(href)').get()
            yield {
                'name': name,
                'description': description,
                'old_price': parse_price(product.css('div.catalog-product__price-old::text').get()),
                'current_price': parse_price(product.css('div.catalog-product__price-actual::text').get()),
                'link': link,
                'image': product.css('div.catalog-product__image img::attr(data-src)').get()
                }

        next_page = response.css('button.pagination-widget__show-more-btn span::text').get()
        if next_page is not None:

            self.i += 1
            next_page = f'https://www.dns-shop.ru/catalog/markdown/?p={self.i}'
            yield SeleniumRequest(url=next_page, callback=self.parse_result, cookies={'city_path': 'chelyabinsk'})

