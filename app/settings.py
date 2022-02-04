from pydantic import BaseSettings


class TelegramNotificationSettings(BaseSettings):
    telegram_token: str
    id: str

    class Config:
        evn_file = ".env"


class TwilioSMSNotificationSettings(BaseSettings):
    twilio_account_sid: str
    twilio_auth_token: str
    from_: str
    to: str

    class Config:
        evn_file = ".env"


class MongoDBSettings(BaseSettings):
    MONGODB_USERNAME: str
    MONGODB_PASSWORD: str
    MONGODB_URI: str
