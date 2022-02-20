import argparse
import scrapy
import crawler.settings
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.spiders.dns import DNSSpider


def parsing_city(city):
    crawler_settings = get_project_settings()
    crawler = CrawlerProcess(settings=crawler_settings)
    crawler.crawl(DNSSpider, city=city)
    crawler.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Markdown updates and send notification')
    parser.add_argument('city',
                        default='chelyabinsk',
                        type=str,
                        help='Name city where markdown updates and send notification'
                        )
    args = parser.parse_args()
    parsing_city(args.city)
