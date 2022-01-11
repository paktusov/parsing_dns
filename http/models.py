from flask_mongoengine import MongoEngine

db = MongoEngine()

class Product(db.Document):
    name = db.StringField(max_length=30, required=True)
    description = db.StringField(max_length=300)
    full_price = db.IntField()
    history_price = db.ListField()
    link = db.URLField()
    image = db.URLField()

    meta = {
        'collection': 'dns_goods',
        'auto_create_index': False,
    }