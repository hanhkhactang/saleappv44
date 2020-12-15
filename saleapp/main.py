from flask import render_template, request, redirect, session, jsonify
from saleapp import app, utils, login, decorator, mail
from saleapp.models import *
from flask_login import login_user
from saleapp.admin import *
import hashlib
import os, json
from flask_mail import Message, Mail

from flask import render_template, request, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message, Mail
from sqlalchemy import func


import hashlib, os, json
from sqlalchemy.exc import IntegrityError
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

randomToken = URLSafeTimedSerializer('this_is_a_secret_key')


@app.route('/')
def index():
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    products = utils.read_products(cate_id=cate_id, kw=kw)

    return render_template('index.html',
                           products=products)



@app.route('/shop')
def shop():
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    products = utils.read_products(cate_id=cate_id, kw=kw)

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
        user = utils.check_login_user(username=username,
                                 password=password)
        admin = utils.check_login(username=username,
                                    password=password)
        if user:
            login_user(user=user)
            return redirect('/')
        if admin:
            login_user(user=admin)
            return redirect('/admin')

    return redirect('/login1')


@app.route('/products/<int:product_id>')
def product_single():
    return render_template('product-single.html')


@app.route("/login-admin", methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', '')
        admin = utils.check_login(username=username,
                                 password=password)
        if admin:
            login_user(user=admin)

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


@app.route('/forgot', methods=['get', 'post'])
@app.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    # Chức năng tìm kiếm trên thanh menu seacrh
    kw = request.args.get('kw')
    if kw:
        return redirect(url_for('search_by_kw', kw=kw))

    err_msg = ""
    if request.method == 'POST':
        try:
            email = request.form.get("email")
            # Nếu check có email của khách hàng trong db
            if utils.check_mail(email=email):
                # Thì chuyển đến trang thông báo đã gửi yêu cầu khôi phục
                return redirect(url_for("request_sent", user_email=email))
            else:
                err_msg = "Nhập sai email"
        except IntegrityError:
            err_msg = "Nhập sai email"

    # Render trang báo đã gửi mail khôi phục
    return render_template("forgot-password.html", err_msg=err_msg)


# Xác thực email người dùng
@app.route('/email-verification/<user_email>', methods=["GET", "POST"])
def email_verify(user_email):
    # Chức năng tìm kiếm trên thanh menu seacrh
    kw = request.args.get('kw')
    if kw:
        return redirect(url_for('search_by_kw', kw=kw))

    # Tạo mã xác thực và gửi mail xác thực
    # Tạo token, dumps salt để tham chiếu với loads salt khi cần xác thực token
    token = randomToken.dumps(user_email, salt="email_confirm")
    # Tạo nội dung email
    msg = Message('Thư xác nhận', sender="hanhkhactang@gmail.com", recipients=[user_email])
    link = url_for('confirm_email', token=token, _external=True)
    msg.body = 'Vui lòng nhấn vào liên kết sau để xác nhận email. Liên kết của bạn là: {}'.format(link)
    # Gửi
    mail.send(msg)

    # Thông báo người dùng là đã gửi email
    return render_template("verify-email.html", user_email=user_email, )


# Xác thực email người dùng
# Khi người dùng nhấn vào liên kết xác thực gửi kèm mail, điều hướng đến đây
# Xác thực email
@app.route('/confirm_email/<token>')
def confirm_email(token):
    # Chức năng tìm kiếm trên thanh menu seacrh
    kw = request.args.get('kw')
    if kw:
        return redirect(url_for('search_by_kw', kw=kw))

    try:
        # Check email loads salt có email dumps salt lúc gửi không
        email = randomToken.loads(token, salt='email_confirm', max_age=900)
    except SignatureExpired:
        return render_template('verify-expired.html')
    return render_template('verify-success.html', email=email)


# Chức năng khôi phục tài khoản qua email
# Thực hiện khi người dùng nhập đúng email có tồn tại trong db
@app.route('/request_sent/<user_email>', methods=["GET", "POST"])
def request_sent(user_email):
    # Chức năng tìm kiếm trên thanh menu seacrh
    kw = request.args.get('kw')
    if kw:
        return redirect(url_for('search_by_kw', kw=kw))

    # Tạo mã xác thực và gửi mail xác thực
    # Tạo token, dumps salt để tham chiếu với loads salt khi cần xác thực token
    token = randomToken.dumps(user_email, salt="recovery_account")
    # Tạo nội dung email
    msg = Message('Khôi phục tài khoản', sender='hanhkhactang@gmail.com', recipients=[user_email])
    link = url_for('recovery_account', token=token, user_email=user_email, _external=True)
    msg.body = 'Bạn đang thực hiện đặt lại mật khẩu, liên kết sẽ hết hạn sau khoảng 15 phút. Nhấn vào liên kết sau ' \
               'để đặt lại mật khẩu: {}'.format(link)
    # Tiến hành gửi mail
    mail.send(msg)

    # Thông báo với khách hàng là đã gửi email khôi phục
    return render_template("recovery-sent.html", user_email=user_email)


# Chức năng khôi phục tài khoản qua email
# Khi khách hàng nhấn vào liên kết được gửi kèm mail, điều hướng đến đây
@app.route('/recovery_account/<token>/<user_email>', methods=['GET', 'POST'])
def recovery_account(token, user_email):
    # Chức năng tìm kiếm trên thanh menu seacrh
    kw = request.args.get('kw')
    if kw:
        return redirect(url_for('search_by_kw', kw=kw))

    try:
        # Kiểm tra token loads salt có bằng với dumps salt lúc gửi hay không, max_age=15phút
        e = randomToken.loads(token, salt='recovery_account', max_age=3600)
    # Nếu token hết hạn trả thông báo cho khách hàng
    except SignatureExpired:
        return render_template('verify-expired.html')
    # Nếu token hơp lệ tiến hành cho người dùng đặt lại mật khẩu
    if request.method == 'POST':
        password = request.form.get("password")
        user = utils.check_mail(user_email)
        if user:
            user.password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
            db.session.add(user)
            db.session.commit()
            # Hiển thị thông báo khôi phục thành công, yêu cầu đăng nhập lại
            return render_template('password-reset.html')

    return render_template('recovery-account.html')


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


@app.route('/api/cart', methods=['post'])
def cart():
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    data = json.loads(request.data)
    id = str(data.get("id"))
    name = data.get("name")
    price = data.get("price")

    if id in cart:
        cart[id]["quantity"] = cart[id]["quantity"] + 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1,
        }

    session['cart'] = cart

    quan, price = utils.cart_stats(cart)

    return jsonify({
        "total_amount": price,
        "total_quantity": quan
    })


@app.route('/payment')
def payment():
    quan, price = utils.cart_stats(session.get('cart'))
    cart_info = {
        "total_amount": price,
        "total_quantity": quan
    }
    return render_template('cart.html',
                           cart_info=cart_info)


@app.route('/api/pay', methods=['post'])
@decorator.login_required
def pay():
    if utils.add_receipt(session.get('cart')):
        del session['cart']

        return jsonify({
            "message": "Add receipt successful!",
            "err_code": 200
        })

    return jsonify({
        "message": "Failed"
    })


if __name__ == '__main__':
    app.run(debug=True)
