import scrapy


class QuotesSpider(scrapy.Spider):
    name = "markdown"

    def start_requests(self):
        urls = [
            'https://apps.chelurban.ru/dns.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'dont_redirect': True},
                                cookies={'city_path': 'chelyabinsk',
                                         #'ipp_key': 'v1640534104243/v3394bd400b5e53a13cfc65163aeca6afa04ab3/hyPrcRNHuXqseT7wjvv8Qg==',
                                         #'ipp_uid': 'v1640534104243/v3394bd400b5e53a13cfc65163aeca6afa04ab3/hyPrcRNHuXqseT7wjvv8Qg==',
                                         #'PHPSESSID': 'e5fe6d8bbfa231f219fc693b8d167ce8',
                                         #'IDE': 'AHWqTUkqihtf7_Ym98p1_45DNLjl3lN5qPCU__scYKM9ZzYBovKEqm26BY5btwqz',
                                         #'VID': '14sOUa11MCo700000Z16H4I7:::0-0-0-6e2e91a:CAASEF9ZRZGzgVhiOZkHxrUVTxoaYGWBl8r3XrOLOT_VZ5CblHCHL0bOpoE7lI7ztCiqb34SfM9JpJLtmN5-CCfWnK4HlAZsz9LwYv0m33k0WAq7kX2_wTGApYFoWn-6ndpNxcXR9_hGvMyC56Yuk0waVxbA0w',
                                         #'cartUserCookieIdent_v3': '01c58abe2a070ea05332564f6235a88c5067aa0eb348fa240a4920450e8d799ba%3A2%3A%7Bi%3A0%3Bs%3A22%3A%22cartUserCookieIdent_v3%22%3Bi%3A1%3Bs%3A36%3A%225d7e0794-57cd-353e-93cf-3f52b8014f45%22%3B%7D',
                                         #'current_path': '3d3cbe8875c96c0a90e902e76a296ae9266d20f500dafd728f18539923f8b9baa%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A132%3A%22%7B%22city%22%3A%22b464725e-819d-11de-b404-00151716f9f5%22%2C%22cityName%22%3A%22%5Cu0427%5Cu0435%5Cu043b%5Cu044f%5Cu0431%5Cu0438%5Cu043d%5Cu0441%5Cu043a%22%2C%22method%22%3A%22geoip%22%7D%22%3B%7D',
                                         #'dnsauth_csrf': '11e479b34151b531d14df2c861a86c41301b395bcfac9e6b3275cee97fac0a64a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22dnsauth_csrf%22%3Bi%3A1%3Bs%3A36%3A%224bd70d9f-dcc8-4c6b-a1ef-5b1c13a2441f%22%3B%7D',
                                         #'i': 'jrx59ph995cPBfuH7L56S3RxwJtRV5a6fb+1lOyQNB+nO8va41p/dYvIy6EXgq63lsdI3kUzjAu2enMnRzYA7Yqrdl8=',
                                         #'ouid': '225501369_3375965164',
                                         #'phonesIdent': '9fdc325dfd6589fdd51359ac8eb25ebfe08aaec12b54b5282e60b18e41f6da08a%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22phonesIdent%22%3Bi%3A1%3Bs%3A36%3A%22d7dcdc51-382b-431b-8f3c-b7a9477c4551%22%3B%7D',
                                         #'rcuid': '61c890599bc008000108d32d',
                                         #'rerf': 'AAAAAGHIkFiInTVUH4duAg==',
                                         #'rrpvid': '261402797678261',
                                         #'tmr_detect': '1%7C1640534942674',
                                         #'tmr_lvid': '02e658175e390b4bc51ee22844299a59',
                                         #'tmr_lvidTS': '1640534131731',
                                         #'tmr_reqNum': '16',
                                         #'wishlist-id': '8c4b2a425b9642d78761edce397dec324868a0237febc845734633c7d4e96f6ca%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22wishlist-id%22%3Bi%3A1%3Bs%3A36%3A%22dd267c48-01ac-44e2-8b04-9cd3f2b4e9ad%22%3B%7D'
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

