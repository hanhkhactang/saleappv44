import json, hashlib
from saleapp.models import User, UserRole, Sach, Receipt, ReceiptDetail, PhieuNhapSach, HoaDonSach
from saleapp import *
from flask_login import current_user


def cart_stats(cart):
    total_quantity, total_amount = 0, 0
    if cart:
        for p in cart.values():
            total_quantity = total_quantity + p["quantity"]
            total_amount = total_amount + p["quantity"] * p["price"]

    return total_quantity, total_amount


def read_data(path='data/categories.json'):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def read_products(cate_id=None, kw=None):
    products = Sach.query

    if cate_id:
        products = products.filter(Sach.catgory_id == cate_id)

    if kw:
        products = products.filter(Sach.name.contains(kw))
    return products.all()

    # if cate_id:
    #     cate_id = int(cate_id)
    #     products = [p for p in products\
    #                 if p['category_id'] == cate_id]
    #
    # if kw:
    #     products = [p for p in products \
    #                 if p['name'].find(kw) >= 0]
    #
    # if from_price and to_price:
    #     from_price = float(from_price)
    #     to_price = float(to_price)
    #     products = [p for p in products \
    #                 if to_price >= p['price'] >= from_price]
    #
    # return products


def get_product_by_id(product_id):
    return Sach.query.get(product_id)
    # products = read_data('data/products.json')
    # for p in products:
    #     if p['id'] == product_id:
    #         return p


def add_user(name, email, username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, email=email,
             username=username, password=password,
             # avatar=avatar_path
             )
    try:
        db.session.add(u)
        db.session.commit()
        return True
    except Exception as ex:
        print(ex)
        return False


# role=UserRole.ADMIN, User.user_role == role
def check_login(username, password, role=UserRole.ADMIN):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = User.query.filter(User.username == username,
                             User.password == password,
                             User.user_role == role).first()

    return user


def check_login_user(username, password, role=UserRole.USER):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = User.query.filter(User.username == username,
                             User.password == password,
                             User.user_role == role).first()

    return user


def cart_stats(cart):
    total_quantity, total_amount = 0, 0
    if cart:
        for p in cart.values():
            total_quantity = total_quantity + p["quantity"]
            total_amount = total_amount + p["quantity"] * p["price"]

    return total_quantity, total_amount


def check_mail(email):
    return User.query.filter(User.email == email).first()


def add_receipt(cart):
    if cart:
        receipt = Receipt(customer_id=1)
        db.session.add(receipt)
        for p in list(cart.values()):
            detail = ReceiptDetail(receipt=receipt,
                                product_id=int(p["id"]),
                                quantity=p["quantity"],
                                price=p["price"])
            db.session.add(detail)

        try:
            db.session.commit()
            return True
        except Exception as ex:
            print(ex)

    return False


def nhap_sach(ngaynhap, idsach , soluong):

    sach = Sach.query.get(idsach)
    p = sach.id

    sls = sach.soluong
    if sls <= int(300) and int(soluong) <= int(400):
        phieunhap =HoaDonSach(ngayNhap=ngaynhap)
        db.session.add(phieunhap)
        detail = PhieuNhapSach(phieunhap = phieunhap,
                                soLuong=soluong,
                                  sach_id = idsach)
        db.session.add(detail)
        soluong.query.filter(p == soluong.sach_id).delete()
        soluongsach = soluong(sach_id = idsach,
                                      soLuong = sls + int(soluong))
        db.session.add(soluongsach)
        try:
            db.session.commit()
            return True
        except Exception as ex:
            print(ex)
    return False



