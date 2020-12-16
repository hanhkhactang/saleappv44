from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from saleapp import admin, db, utils
from saleapp.models import Category, Sach, TacGia, PhieuThu, LogoutView, ContactView, PhieuNhapSach, HoaDonSach, User, UserRole
from flask_login import current_user, UserMixin
from sqlalchemy.orm import relationship, backref
from saleapp import db
from flask_login import UserMixin, logout_user, current_user, login_user
from flask_admin import BaseView, expose
from flask import redirect, request


class CategoryModelView(ModelView):
        def is_accessible(self):
            return current_user.is_authenticated


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated



class ContactView(BaseView):
    @expose('/')
    def index(self):
        cate_id = request.args.get('category_id')
        kw = request.args.get('kw')
        products = utils.read_products(cate_id=cate_id, kw=kw)
        return self.render('admin/contact.html', products=products)

    def is_accessible(self):
        return current_user.is_authenticated


class NhapSachView(BaseView):
    @expose('/', methods=['post','get'])
    def indexpn(self):
        err_msg = ""
        sach = utils.read_products()
        if request.method == 'POST':
            ngay = request.form.get("date")
            soluong = request.form.get('soLuong')
            idsach = request.form.get('idsach')
            if utils.nhap_sach(ngaynhap=ngay, soluong=soluong, idsach=idsach):
                    err_msg = "Nhập Sách Thành Công!"
            else:
                err_msg = "Nhập Không Thành công!"
        return self.render('admin/product.html', sach=sach, err_msg=err_msg)

    def is_accessible(self):
            return current_user.is_authenticated


admin.add_view(CategoryModelView(Category, db.session))
admin.add_view(CategoryModelView(Sach, db.session))
admin.add_view(NhapSachView(name="Nhập Sách"))
admin.add_view(CategoryModelView(TacGia, db.session))
admin.add_view(CategoryModelView(PhieuThu, db.session))
admin.add_view(ContactView(name='Liên hệ'))
admin.add_view(LogoutView(name="Đăng xuất"))

