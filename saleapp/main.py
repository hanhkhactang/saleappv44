from flask import render_template, request, redirect, session, jsonify
from saleapp import app, utils, login
from saleapp.models import *
from flask_login import login_user
from saleapp.admin import *
import hashlib
import os, json


@app.route('/')
def index():
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    products = utils.read_products(cate_id=cate_id, kw=kw, from_price=from_price, to_price=to_price)

    return render_template('index.html',
                           products=products)



@app.route('/shop')
def shop():
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    products = utils.read_products(cate_id=cate_id, kw=kw, from_price=from_price, to_price=to_price)

    return render_template('shop.html',
                           products=products)


@app.route('/logout')
def logout():
    logout_user()
    session.pop('user',None)
    return redirect('/')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/login1')
def login1():
    return render_template('login1.html')


@app.route('/login', methods=['post', 'get'])
def login12():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', '')
        kh = utils.check_login_user(username=username,
                                 password=password)
        if kh:
            login_user(user=kh)
            return redirect('/')

    return redirect('/login1')


@app.route('/products/<int:product_id>')
def product_single():
    return render_template('product-single.html')


@app.route("/login-admin", methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', '')
        user = utils.check_login(username=username,
                                 password=password)
        if user:
            login_user(user=user)

    return redirect('/admin')


@app.route('/login', methods=['post', 'get'])
def login_usr():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', '')
        kh = utils.check_login(username=username,
                                 password=password)
        if kh:
            login_user(user=kh)
            return redirect('/')

    return redirect('/admin')


@expose('/')
def login123(self):
     logout_user()

     return redirect("/")


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ""
    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password == confirm:
            name = request.form.get('name')
            email = request.form.get('email')
            username = request.form.get('username')
            # avatar = request.files["avatar"]
            #
            # avatar_path = 'images/upload/%s' % avatar.filename
            # avatar.save(os.path.join(app.root_path,
            #                          'static/',
            #                          avatar_path))avatar_path=avatar_path
            if utils.add_user(name=name, email=email, username=username,
                              password=password):
                return redirect('/')
            else:
                err_msg = "Hệ thống đang có lỗi! Vui lòng quay lại sau!"
        else:
            err_msg = "Mật khẩu KHÔNG khớp!"

    return render_template('register.html', err_msg=err_msg)




@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# @app.route('/products')
# def product_list():
#     cate_id = request.args.get('category_id')
#     kw = request.args.get('kw')
#     from_price = request.args.get('from_price')
#     to_price = request.args.get('to_price')
#     products = utils.read_products(cate_id=cate_id, kw=kw, from_price=from_price, to_price=to_price)
#
#     return render_template('product-list.html',
#                            products=products)


@app.route('/shop/<int:product_id>')
def product_detail(product_id):
    product = utils.get_product_by_id(product_id=product_id)
    return render_template('product-single.html',
                           product=product)


if __name__ == '__main__':
    app.run(debug=True)
