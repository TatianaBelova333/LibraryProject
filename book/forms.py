from django import forms
from django.core.exceptions import ValidationError

from book.models import Reader, Book


class ReaderForm(forms.ModelForm):
    """Reader admin form."""

    class Meta:
        model = Reader
        fields = '__all__'

    def clean_borrowed_books(self):
        """
        Validate that the reader can only borrow a specific number of books
        defined by the max_book_count variable.

        """
        borrowed_books = self.cleaned_data.get('borrowed_books')
        max_book_count = 3
        if borrowed_books and borrowed_books.count() > max_book_count:
            raise ValidationError('Читатель может взять не больше 3 книг.')
        return self.cleaned_data
