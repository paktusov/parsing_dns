import datetime as dt

from mongo import get_db

if __name__ == '__main__':
    db = get_db()

    for city in db['cities'].find():
        products = db[city["name"]].find()
        for product in products:
            for i in range(len(product["history_price"])):
                if isinstance(product["history_price"][i][1], str):
                    product["history_price"][i][1] = dt.datetime.fromisoformat(product["history_price"][i][1])
            if isinstance(product['last_update'], str):
                product['last_update'] = dt.datetime.fromisoformat(product['last_update'])
            db[city["name"]].find_one_and_replace({"_id": product["_id"]}, product)
        print(city["name"])
