from django import forms
from django.core.exceptions import ValidationError

from book.models import Reader, Book


class ReaderForm(forms.ModelForm):
    """Reader admin form."""

    def __init__(self, *args, **kwargs):
        """Override borrowed_books field for the Reader model.
        Return books that are on the reader's hands or/and available in the library."""
        super().__init__(*args, **kwargs)
        self.fields['borrowed_books'].queryset = (Book.objects.filter(amount__gt=0)
                                                  | self.instance.borrowed_books.all())

    class Meta:
        model = Reader
        fields = '__all__'

    def clean(self):
        """
        Validate that the reader can only borrow a specific number of books
        defined by the max_book_count variable.

        """
        borrowed_books = self.cleaned_data.get('borrowed_books')
        max_book_count = 3
        if borrowed_books and borrowed_books.count() > max_book_count:
            raise ValidationError('Читатель может взять не больше 3 книг.')
        return self.cleaned_data
