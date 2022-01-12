from flask_mongoengine import MongoEngine

db = MongoEngine()

class Product(db.Document):
    name = db.StringField(max_length=30, required=True)
    description = db.StringField(max_length=300)
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
