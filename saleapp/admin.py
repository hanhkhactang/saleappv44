from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from saleapp import admin, db
from saleapp.models import Category, Sach, KhachHang, TacGia, PhieuThu


class ContactView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/contact.html')


class CategoryModelView(ModelView):
    column_display_pk = False
    can_create = True
    can_edit = True
    can_export = True
    can_delete = False
    can_export = True
    form_columns = ('name', )



admin.add_view(CategoryModelView(Category, db.session))
admin.add_view(CategoryModelView(Sach, db.session))
admin.add_view(CategoryModelView(KhachHang, db.session))
admin.add_view(CategoryModelView(TacGia, db.session))
admin.add_view(ModelView(PhieuThu, db.session))
admin.add_view(ContactView(name='Liên hệ'))
