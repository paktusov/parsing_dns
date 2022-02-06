from typing import Optional
import datetime as dt
import pytz
import scrapy
import re
from selenium import webdriver
from scrapy_selenium import SeleniumRequest
from crawler.items import ProductItem


def parse_price(price: str) -> Optional[int]:
    if not price:
        return None
    return int(re.sub(r"\D+", "", price))

cities = {'chelyabinsk': {'city_path': 'chelyabinsk',
                          'current_path': 'c52dd52d7f531f1b3358bf7d20d16797b8e3fefecf1a1718df7ffd0ded046ccca%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A133%3A%22%7B%22city%22%3A%22b464725e-819d-11de-b404-00151716f9f5%22%2C%22cityName%22%3A%22%5Cu0427%5Cu0435%5Cu043b%5Cu044f%5Cu0431%5Cu0438%5Cu043d%5Cu0441%5Cu043a%22%2C%22method%22%3A%22manual%22%7D%22%3B%7D'
                          },
          'ekaterinburg': {'city_path': 'ekaterinburg',
                           'current_path': '36eb258224635d8576f70f8642463a7b152cde72592e0338559443f7d4a0d736a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A151%3A%22%7B%22city%22%3A%2283878977-f329-11dd-9648-00151716f9f5%22%2C%22cityName%22%3A%22%5Cu0415%5Cu043a%5Cu0430%5Cu0442%5Cu0435%5Cu0440%5Cu0438%5Cu043d%5Cu0431%5Cu0443%5Cu0440%5Cu0433%22%2C%22method%22%3A%22manual%22%7D%22%3B%7D'
                           },
          'moscow': {'city_path': 'moscow',
                     'current_path': '605bfdc517d7e9e23947448a9bf1ce16ac36b884434a3fdb10db053793c50392a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A115%3A%22%7B%22city%22%3A%2230b7c1f3-03fb-11dc-95ee-00151716f9f5%22%2C%22cityName%22%3A%22%5Cu041c%5Cu043e%5Cu0441%5Cu043a%5Cu0432%5Cu0430%22%2C%22method%22%3A%22manual%22%7D%22%3B%7D'
                     }
          }

class DNSSpider(scrapy.Spider):
    driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub')
    driver.get("https://www.dns-shop.ru/")
    driver.add_cookie({"name": 'city_path', "value": 'ekaterinburg'})
    driver.add_cookie({"name": 'current_path', "value": '36eb258224635d8576f70f8642463a7b152cde72592e0338559443f7d4a0d736a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A151%3A%22%7B%22city%22%3A%2283878977-f329-11dd-9648-00151716f9f5%22%2C%22cityName%22%3A%22%5Cu0415%5Cu043a%5Cu0430%5Cu0442%5Cu0435%5Cu0440%5Cu0438%5Cu043d%5Cu0431%5Cu0443%5Cu0440%5Cu0433%22%2C%22method%22%3A%22manual%22%7D%22%3B%7D'})
    print(driver.get_cookies())
    driver.quit()

    name = "dns"
    i = 1
    collection_name = 'ekaterinburg'


    def start_requests(self):
        url = f'https://www.dns-shop.ru/catalog/markdown/?p={self.i}'
        yield SeleniumRequest(url=url, callback=self.parse_result)

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
