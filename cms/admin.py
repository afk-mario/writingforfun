from django.contrib import admin
from adminsortable.admin import SortableAdmin
from .models import *

@admin.register(Entry)
class ProductAdmin(SortableAdmin):
    pass

@admin.register(Post)
class ProductAdmin(SortableAdmin):
    pass
