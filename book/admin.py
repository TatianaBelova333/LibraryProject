from django.contrib import admin

from book.forms import ReaderForm
from book.models import Author, Book, Reader


class ReaderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'is_active')
    form = ReaderForm


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('last_name',)


class BookAdmin(admin.ModelAdmin):
    list_filter = ('title', 'author__last_name')
    list_display = (
        'title',
        'author',
        'amount',
    )


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Reader, ReaderAdmin)
