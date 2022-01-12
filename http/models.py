from flask_mongoengine import MongoEngine

db = MongoEngine()

class Product(db.Document):
    name = db.StringField(required=True)
    description = db.StringField()
    full_price = db.IntField()
    history_price = db.ListField()
    link = db.URLField(required=True)
    image = db.URLField()
    last_update = db.DateTimeField(required=True)
    last_seen = db.DateTimeField(required=True)

    meta = {
        'collection': 'dns_goods',
        'auto_create_index': False,
    }
