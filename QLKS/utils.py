import json, hashlib
from QLKS import db
from QLKS.models import User


def read_data(path='data/categories.json'):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def read_products(category_id=None, kw=None,
                  from_price=None, to_price=None):
    products = read_data(path='data/products.json')

    if category_id:
        category_id = int(category_id)
        products = [p for p in products if p['category_id'] == category_id]

    if kw:
        products = [p for p in products if p['name'].find(kw) >= 0]

    if from_price and to_price:
        from_price = float(from_price)
        to_price = float(to_price)

        products = [p for p in products if p['price'] >= from_price and p['price'] <= to_price]


    return products


def get_product_by_id(product_id):
    products = read_data(path='data/products.json')
    for p in products:
        if p["id"] == product_id:
            return p


def add_user(name, email, username, password, avatar):
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    u = User(name=name, email=email, username=username,
             password=password, avatar=avatar)
    try:
        db.session.add(u)
        db.session.commit()

        return True
    except Exception as ex:
        print(ex)
        return False
