from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Table, DateTime, Enum
from sqlalchemy.orm import relationship, backref
from saleapp import db
from flask_login import UserMixin, logout_user, current_user
from flask_admin import BaseView, expose
from flask import redirect
from enum import Enum as UserEnum


class SaleBase(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable= False)


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2


class User(SaleBase, UserMixin):
    __tablename__ = 'user'
    email = Column(String(100))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    # avatar = Column(String(100))
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='customer', lazy=True)


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return self.render("/admin")


class Category(SaleBase):
    __tablename__ = 'category'


class Sach(SaleBase):
    __tablename__ = 'Book'
    soluong = Column(Integer, default=0)
    image = Column(String(100))
    gia = Column(Float)
    descrip = Column(String(255))
    category = relationship('Category', secondary='theloaisach', lazy = 'subquery', backref=backref('Book', lazy=True))
    tacgia_id = Column(Integer, ForeignKey('TacGia.id'), nullable=False)
    receipt_details = relationship('ReceiptDetail', backref='Book', lazy=True)

    def __repr__(self) -> str:
        return repr(self.name)




class HoaDonSach(db.Model):
    __tablename__ = 'HoaDonSach'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngaynhap = Column(DateTime)
    decreption = Column(String(255))


class PhieuNhapSach(db.Model):
    Book_id = Column(Integer, ForeignKey('Book.id'),primary_key=True)
    HoaDonSach_id = Column(Integer, ForeignKey('HoaDonSach.id'),primary_key=True)
    soluongnhap = Column(Integer)


# PhieuNhapSach = db.Table('PhieuNhapSach',
#                          Column('Book_id', Integer, ForeignKey('Book.id'), primary_key=True),
#                          Column('HoadonSach_id', Integer, ForeignKey('HoaDonSach.id'), primary_key=True),
#                          Column('SoLuongNhap', Integer),
#                          Column('NgayNhap', DateTime))


theloaisach = db.Table('theloaisach',
    Column('Book_id', Integer, ForeignKey('Book.id'), primary_key=True),
    Column('Cat_id', Integer, ForeignKey('category.id'), primary_key=True))


#
# HoaDon = db.Table('HoaDon',
#     Column('Book_id', Integer, ForeignKey('Book.id'), primary_key=True),
#     Column('KhachHang_id', Integer, ForeignKey('KhachHang.id'), primary_key=True),
#     Column('SoLuongBan', Integer),
#     Column('DonGia', Float),
#     Column('TongTien', Float))
class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.today())
    customer_id = Column(Integer, ForeignKey(User.id))
    details = relationship('ReceiptDetail',
                           backref='receipt', lazy=True)


class ReceiptDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Sach.id), nullable=False)
    quantity = Column(Integer, default=0)
    price = Column(Integer, default=0)

    def __repr__(self) -> str:
        return repr(self.id)


class TacGia(SaleBase):
    __tablename__ = 'TacGia'
    Book = relationship('Sach', backref='TacGia', lazy = True)

    def __repr__(self):
        return repr(self.name)

    def is_accessible(self):
        return current_user.is_authenticated


class PhieuThu(db.Model):
    __tablename__ = 'PhieuThu'
    PhieuThu_id = Column(Integer, primary_key=True, autoincrement=True)
    NgayLap = Column(DateTime)
    SoTienThu = Column(Float)
    KhachHang_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def is_accessible(self):
        return current_user.is_authenticated


class ContactView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/contact.html')

    def is_accessible(self):
        return current_user.is_aurhenticated


if __name__ == '__main__':
    db.create_all()