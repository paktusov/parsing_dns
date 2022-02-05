import os
from pydantic import BaseSettings
from dotenv import load_dotenv
load_dotenv()

class TelegramNotificationSettings(BaseSettings):
    telegram_token: str
    id: str

    class Config:
        evn_file = ".env"
        env_file_encoding = 'utf-8'


class TwilioSMSNotificationSettings(BaseSettings):
    twilio_account_sid: str
    twilio_auth_token: str
    from_: str
    to: str

    class Config:
        evn_file = ".env"
        env_file_encoding = 'utf-8'


class MongoDBSettings(BaseSettings):
    MONGODB_USERNAME: str
    MONGODB_PASSWORD: str
    MONGODB_URI: str

    class Config:
        evn_file = ".env"
        env_file_encoding = 'utf-8'


telegram_config = TelegramNotificationSettings()
twilio_config = TwilioSMSNotificationSettings()
mongo_config = MongoDBSettings()
