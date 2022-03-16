import math

import pymongo
from flask import Flask, render_template, request, url_for
from flask_paginate import Pagination, get_page_parameter
from mongo import get_db

app = Flask(__name__)
app.debug = True
db = get_db()

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
    page = request.args.get(get_page_parameter(), 1, type=int)
    per_page = 50
    offset = (page - 1) * per_page
    limit = per_page
    kwargs = dict(request.args)
    kwargs.pop('page', None)
    current_products = list(products.sort("last_update", pymongo.DESCENDING).skip(offset).limit(limit))
    pagination = Pagination(page=page, total=count, record_name='products', per_page=per_page)
    return render_template(
        'index.html',
        products=current_products,
        title=title,
        header=header,
        keyword=keyword,
        kwargs=kwargs,
        current_city=current_city,
        cities=cities_name,
        pagination=pagination,
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0')
