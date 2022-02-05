import math
import datetime as dt
import pymongo
from flask import Flask, render_template, request, url_for, redirect
from config import mongo_config


app = Flask(__name__)
app.debug = True

client = pymongo.MongoClient(
    mongo_config.uri,
    username=mongo_config.username,
    password=mongo_config.password
)
db = client[mongo_config.database]
collection_name = 'chelyabinsk'


@app.route('/')
def index():
    title = 'Markdown'
    header = 'Markdown'
    keyword = request.args.get('keyword', '', type=str)
    products = db[collection_name].find({"name": {'$regex': keyword, '$options': 'i'}})
    count = db[collection_name].count_documents({"name": {'$regex': keyword, '$options': 'i'}})
    page = request.args.get('page', 1, type=int)
    per_page = 40
    pages = math.ceil(count // per_page)
    offset = (page - 1) * per_page
    limit = per_page
    kwargs = dict(request.args)
    kwargs.pop('page', None)
    prev_url = url_for('index', page=page-1, **kwargs) if page > 1 else None
    next_url = url_for('index', page=page+1, **kwargs) if page < pages else None
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
        kwargs=kwargs
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0')
