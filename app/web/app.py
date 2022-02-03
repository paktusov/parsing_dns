import math
import datetime as dt
import pymongo
from flask import Flask, render_template, request, url_for, redirect
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.debug = True

mongo_uri = os.getenv('MONGODB_URI')
mongo_username = os.getenv('MONGODB_USERNAME')
mongo_password = os.getenv('MONGODB_PASSWORD')
client = pymongo.MongoClient(
    mongo_uri,
    username=mongo_username,
    password=mongo_password
)
db = client['parsing_dns']
collection_name = 'dns_goods'


@app.route('/')
def index():
    title = 'Markdown'
    header = 'Markdown'
    keyword = request.args.get('keyword', '', type=str)
    products = db[collection_name].find({"name": {'$regex': keyword, '$options': 'i'}})
    count = products.count()
    page = request.args.get('page', 1, type=int)
    per_page = 40
    pages = math.ceil(count // per_page)
    offset = (page - 1) * per_page
    limit = per_page
    prev_url = url_for('index', page=page-1, keyword=keyword) if page > 1 else None
    next_url = url_for('index', page=page+1, keyword=keyword) if page < pages else None
    current_products = list(products.sort("last_update", pymongo.DESCENDING).skip(offset).limit(limit))
    for i in range(len(current_products)):
        current_products[i]['last_update'] = dt.datetime.fromisoformat(current_products[i]['last_update'])
    return render_template(
        'index.html',
        products=current_products,
        title=title,
        header=header,
        page=page,
        prev_url=prev_url,
        next_url=next_url,
        pages=pages,
        keyword=keyword,
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0')
