import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class TelegramNotificationSettings(BaseSettings):
    token_chelyabinsk: str
    token_ekaterinburg: str
    id: str

    class Config:
        evn_file = ".env"
        env_prefix = 'telegram_'


class TwilioSMSNotificationSettings(BaseSettings):
    account_sid: str
    auth_token: str
    from_: str
    to: str

    class Config:
        evn_file = ".env"
        env_prefix = 'twilio_'


class MongoDBSettings(BaseSettings):
    username: str
    password: str
    uri: str
    database: str

    class Config:
        evn_file = ".env"
        env_prefix = 'mongodb_'


class CelerySettings(BaseSettings):
    broker: str = 'redis://redis'
    timezone: str = 'Asia/Yekaterinburg'
    worker_max_tasks_per_child: int = 1
    broker_pool_limit: bool = None


class SeleniumSettings(BaseSettings):
    driver_name: str = 'chrome'
    command_executor: str = 'http://selenium:4444/wd/hub'
    driver_arguments: list = ['--headless']


telegram_config = TelegramNotificationSettings()
twilio_config = TwilioSMSNotificationSettings()
mongo_config = MongoDBSettings()
celery_config = CelerySettings()
selenium_config = SeleniumSettings()
