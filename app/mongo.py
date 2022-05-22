import pymongo
from config import mongo_config


def get_db():
    client = pymongo.MongoClient(
        mongo_config.uri,
        connect=False
    )
    return client[mongo_config.database]
