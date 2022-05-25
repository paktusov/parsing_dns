import pymongo
from config import mongo_config


def get_db():
    client = pymongo.MongoClient(
        mongo_config.uri,
        username=mongo_config.username,
        password=mongo_config.password,
        connect=False
    )
    return client[mongo_config.database]
