import datetime as dt
import pymongo

now = (dt.datetime.now() - dt.timedelta(minutes=20)).isoformat()
print(now)

client = pymongo.MongoClient('mongodb://localhost:2717')
db = client['parsing_dns']
collection_name = 'dns_goods'

db[collection_name].update_many({'last_seen': {'$lt': now}}, {'$set': {'remote': 'True'}})

