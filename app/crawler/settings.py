from shutil import which
from config import mongo_config, selenium_config

BOT_NAME = 'crawler'
SPIDER_MODULES = ['crawler.spiders']

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800,
}

# Configure item pipelines
ITEM_PIPELINES = {
    'crawler.pipelines.MongoPipeline': 300,
}

SELENIUM_DRIVER_NAME = selenium_config.driver_name
SELENIUM_COMMAND_EXECUTOR = selenium_config.command_executor
SELENIUM_DRIVER_ARGUMENTS = selenium_config.driver_arguments
