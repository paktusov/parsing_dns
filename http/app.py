import datetime as dt
from flask import Flask, render_template
from models import db, Product


app = Flask(__name__)

app.config['MONGODB_HOST'] = 'mongodb://localhost:2717/parsing_dns'
app.debug = True

db.init_app(app)

@app.route('/')
def index():
    products = Product.objects().order_by('-last_update')
#    for product in products:
#        product.last_seen = dt.datetime.fromisoformat(product.last_seen)
#        product.last_update = dt.datetime.fromisoformat(product.last_update)
#        product.save()
    return render_template('index.html', products=products)

if __name__ == "__main__":
    app.run()
