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
    category = relationship('Category', secondary='theloaisach', lazy = 'subquery', backref=backref('Book', lazy=True))
    tacgia_id = Column(Integer, ForeignKey('TacGia.id'), nullable=False)
    hoadon = relationship('HoaDonSach', secondary='PhieuNhapSach', lazy='subquery', backref=backref('Book', lazy=True))


class HoaDonSach(db.Model):
    __tablename__ = 'HoaDonSach'
    id = Column(Integer, primary_key=True, autoincrement=True)
    decreption = Column(String(255))


PhieuNhapSach = db.Table('PhieuNhapSach',
                         Column('Book_id', Integer, ForeignKey('Book.id'), primary_key=True),
                         Column('HoadonSach_id', Integer, ForeignKey('HoaDonSach.id'), primary_key=True),
                         Column('SoLuongNhap', Integer),
                         Column('NgayNhap', DateTime))


theloaisach = db.Table('theloaisach',
    Column('Book_id', Integer, ForeignKey('Book.id'), primary_key=True),
    Column('Cat_id', Integer, ForeignKey('category.id'), primary_key=True))


class KhachHang(SaleBase):
    __tablename__ = 'KhachHang'
    DiaChi = Column(String(255))
    SDT = Column(Integer)
    Email = Column(String(50))
    phieuthu = relationship('PhieuThu', backref='KhachHang', lazy=True)


HoaDon = db.Table('HoaDon',
    Column('Book_id', Integer, ForeignKey('Book.id'), primary_key=True),
    Column('KhachHang_id', Integer, ForeignKey('KhachHang.id'), primary_key=True),
    Column('SoLuongBan', Integer),
    Column('DonGia', Float),
    Column('TongTien', Float))


class TacGia(SaleBase):
    __tablename__ = 'TacGia'
    Book = relationship('Sach', backref='TacGia', lazy = True)

    def is_accessible(self):
        return current_user.is_authenticated


class PhieuThu(db.Model):
    __tablename__ = 'PhieuThu'
    PhieuThu_id = Column(Integer, primary_key=True, autoincrement=True)
    NgayLap = Column(DateTime)
    SoTienThu = Column(Float)
    KhachHang_id = Column(Integer, ForeignKey('KhachHang.id'), nullable=False)

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