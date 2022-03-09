import argparse

from crawler.spiders.dns import DNSSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Markdown updates and send notification')
    parser.add_argument('city',
                        default='chelyabinsk',
                        type=str,
                        help='Name city where markdown updates and send notification'
                        )
    args = parser.parse_args()

    process = CrawlerProcess(get_project_settings())
    process.crawl(DNSSpider, city=args.city)
    process.start()
