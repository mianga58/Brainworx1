from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib import admin

from .models import Book


class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        fields = ('id', 'book')


admin.site.register(Book)