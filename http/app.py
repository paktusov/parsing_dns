import datetime as dt
import pymongo
from flask import Flask, render_template

app = Flask(__name__)

client = pymongo.MongoClient('mongodb://localhost:2717')
db = client['parsing_dns']
collection_name = 'dns_goods'
app.debug = True



@app.route('/')
def index():
    title = 'Markdown'
    header = 'Markdown'
    products = list(db[collection_name].find().sort("last_update", pymongo.DESCENDING))
    for i in range(len(products)):
        products[i]['last_update'] = dt.datetime.fromisoformat(products[i]['last_update']).strftime("%Y.%m.%d %H:%M")
    return render_template('index.html', products=products, title=title, header=header)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
