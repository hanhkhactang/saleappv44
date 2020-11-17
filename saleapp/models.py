from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, backref
from saleapp import db
from flask_login import UserMixin, logout_user, current_user
from flask_admin import BaseView, expose


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True,
    autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class SaleBase(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable= False)


class Category(SaleBase):
    __tablename__ = 'category'


class Sach(SaleBase):
    __tablename__ = 'Book'
    soluong = Column(Integer, default=0)
    image = Column(String(100))
    gia = Column(Float)
    category = relationship('Category', secondary ='theloaisach', lazy = 'subquery', backref = backref('Book', lazy=True))
    tacgia_id = Column(Integer, ForeignKey('TacGia.id'), nullable=False)


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
    Column('SoLuongBang', Integer),
    Column('DonGia', Float),
    Column('TongTien', Float))


class TacGia(SaleBase):
    __tablename__ = 'TacGia'
    Book = relationship('Sach', backref='TacGia', lazy = True)


class PhieuThu(db.Model):
    PhieuThu_id = Column(Integer, primary_key=True, autoincrement=True)
    NgayLap = Column(DateTime)
    SoTienThu = Column(Float)
    KhachHang_id = Column(Integer, ForeignKey('KhachHang.id'), nullable=False)


class ContactView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/contact.html')

    def is_accessible(self):
        return current_user.is_aurhenticated()


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()

        return self.render("admin")

    def is_accessible(self):
        return current_user.is_aurhenticated()


if __name__ == '__main__':
    db.create_all()