import os
from pydantic import BaseSettings
from dotenv import load_dotenv
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


telegram_config = TelegramNotificationSettings()
twilio_config = TwilioSMSNotificationSettings()
mongo_config = MongoDBSettings()
