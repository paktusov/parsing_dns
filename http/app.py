import datetime as dt
import pymongo
from flask import Flask, render_template

app = Flask(__name__)

client = pymongo.MongoClient('mongodb://localhost:2717')
db = client['parsing_dns']
collection_name = 'dns_goods'
app.debug = True

#db.init_app(app)

@app.route('/')
def index():
    products = db[collection_name].find().sort("last_update", pymongo.DESCENDING)
#    products = Product.objects().order_by('-last_update')
#    for product in products:
#        product.last_seen = dt.datetime.fromisoformat(product.last_seen)
#        product.last_update = dt.datetime.fromisoformat(product.last_update)
#        product.save()
    return render_template('index.html', products=products)

if __name__ == "__main__":
    app.run()
