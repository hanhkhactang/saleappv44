from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from saleapp import admin, db, utils
from saleapp.models import Category, Sach, TacGia, PhieuThu, LogoutView, ContactView, PhieuNhapSach, HoaDonSach,User,UserRole
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
        return self.render('admin/contact.html')

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(CategoryModelView(Category, db.session))
admin.add_view(CategoryModelView(Sach, db.session))
admin.add_view(CategoryModelView(HoaDonSach, db.session))
admin.add_view(CategoryModelView(TacGia, db.session))
admin.add_view(CategoryModelView(PhieuThu, db.session))
admin.add_view(ContactView(name='Liên hệ'))
admin.add_view(LogoutView(name="Đăng xuất"))

