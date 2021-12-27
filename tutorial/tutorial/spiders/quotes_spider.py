import scrapy


class QuotesSpider(scrapy.Spider):
    name = "markdown"

    def start_requests(self):
        urls = [
            'https://www.dns-shop.ru/catalog/markdown/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'dont_redirect': True},
                                cookies={'city_path': 'chelyabinsk',
                                         'ipp_key': 'v1640534104243/v3394bd400b5e53a13cfc65163aeca6afa04ab3/hyPrcRNHuXqseT7wjvv8Qg==',
                                         'ipp_uid': 'v1640534104243/v3394bd400b5e53a13cfc65163aeca6afa04ab3/hyPrcRNHuXqseT7wjvv8Qg==',
                                        }
                                 )


    def parse(self, response):
        for product in response.css('div.catalog-product'):
            yield {
                'name': product.css('a.catalog-product__name.ui-link.ui-link_black span::text').get(),
                'old_price': product.css('div.catalog-product__price-old::text').get(),
                'current_price': product.css('div.catalog-product__price-actual::text').get(),
                'link': 'https://www.dns-shop.ru' + product.css('a.catalog-product__name.ui-link.ui-link_black::attr(href)').get(),
                'image': product.css('div.catalog-product__image img::attr(data-src)').get()
                }

#        next_page = response.css('li.next a::attr(href)').get()
#        if next_page is not None:
#            next_page = response.urljoin(next_page)
#            yield scrapy.Request(next_page, callback=self.parse, cookies={'city_path': 'chelyabinsk'})

