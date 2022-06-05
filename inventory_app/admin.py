from django.contrib import admin
from .models import Item
from .form import Itemlist
from .models import Csv, Issue


class ItemCreateAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'quantity']
    form = Itemlist


admin.site.register(Item, ItemCreateAdmin)

admin.site.register(Csv)