import datetime as dt
from scrapy.crawler import CrawlerProcess
from crawler.product.spiders.product_spider import ProductSpider
from flask import Flask, render_template
from models import db, Product


app = Flask(__name__)

app.config['MONGODB_HOST'] = 'mongodb://localhost:2717/parsing_dns'
app.debug = True

db.init_app(app)

@app.route('/')
def index():
    products = Product.objects().order_by('name')
    return render_template('index.html', products=products)

if __name__ == "__main__":


    process = CrawlerProcess(get_project_settings())

    process.crawl(ProductSpider)
    process.start()

    app.run()