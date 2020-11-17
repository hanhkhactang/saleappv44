from flask import render_template, request, redirect
from saleapp import app, utils, login
from saleapp.models import *
from flask_login import login_user


@app.route('/')
def index():
    categories = utils.read_data()
    return render_template('index.html',
                           categories=categories)


@app.route("/login-admin", methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter(User.username == username.strip(),
            User.password == password.strip()).first()
        if user:
            login_user(user=user)

    return redirect("/admin")


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/products')
def product_list():
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    products = utils.read_products(cate_id=cate_id, kw=kw, from_price=from_price, to_price=to_price)

    return render_template('product-list.html',
                           products=products)


@app.route('/products/<int:product_id>')
def product_detail(product_id):
    product = utils.get_product_by_id(product_id=product_id)
    return render_template('product-detail.html',
                           product=product)


if __name__ == '__main__':
    app.run(debug=True)
