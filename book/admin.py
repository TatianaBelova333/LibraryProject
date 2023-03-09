from django.contrib import admin
from django.db.models import Case, Value, When, F
from django.urls import reverse
from django.utils.html import format_html, urlencode

from book.models import Author, Book, Reader


class ReaderAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'phone_number',
        'is_active',
        'display_borrowed_books',
    )
    list_filter = ('is_active',)
    actions = ('change_status', 'remove_borrowed_books')

    @admin.action(description='Изменить статус читателя')
    def change_status(self, request, queryset):
        queryset.update(is_active=Case(
            When(is_active=False, then=Value(True)),
            When(is_active=True, then=Value(False)),
        ))

    @admin.action(description='Удалить все книги у читателя')
    def remove_borrowed_books(self, request, queryset):
        for reader in queryset:
            reader_books = reader.borrowed_books.values_list('id', flat=True)
            Book.objects.filter(id__in=reader_books).update(amount=F('amount') + 1)
            reader.borrowed_books.clear()


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('last_name',)


class BookAdmin(admin.ModelAdmin):
    list_filter = ('title', 'author__last_name')
    list_display = (
        'title',
        'author_link',
        'amount',
    )
    list_display_links = ('title',)

    def author_link(self, obj):
        author = obj.author
        url = reverse('admin:book_author_changelist') + str(author.id)
        return format_html(f'<a href="{url}">{author}</a>')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Reader, ReaderAdmin)
