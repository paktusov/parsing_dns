import pymongo
from config import mongo_config

client = pymongo.MongoClient(
    mongo_config.uri,
    username=mongo_config.username,
    password=mongo_config.password
)
db = client[mongo_config.database]
