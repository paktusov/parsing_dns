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


@app.route('/')
def index():
    title = 'Markdown'
    header = 'Markdown'
    cities_name = [city['name'] for city in db['cities'].find()]
    current_city = request.args.get('city', 'chelyabinsk', type=str)
    keyword = request.args.get('keyword', '', type=str)
    query = dict()
    if keyword:
        query['name'] = {'$regex': keyword, '$options': 'i'}
    products = db[current_city].find(query)
    count = db[current_city].count_documents(query)
    page = request.args.get('page', 1, type=int)
    per_page = 50
    pages = math.ceil(count // per_page)
    offset = (page - 1) * per_page
    limit = per_page
    kwargs = dict(request.args)
    kwargs.pop('page', None)
    prev_url = url_for('index', page=page-1, **kwargs) if page > 1 else None
    next_url = url_for('index', page=page+1, **kwargs) if page < pages else None
    current_products = list(products.sort("last_update", pymongo.DESCENDING).skip(offset).limit(limit))
    for i in range(len(current_products)):
        if isinstance(current_products[i]['last_update'], str):
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
        kwargs=kwargs,
        current_city=current_city,
        cities=cities_name
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0')
