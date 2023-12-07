from django.contrib import admin

from converter.models import Converter


# Register your models here.
@admin.register(Converter)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'code', 'created', 'changed', 'converter_user')
    list_display_links = ('id',)
    search_fields = ('title', 'code', 'converter_user')
    list_filter = ('title', 'code', 'converter_user')
