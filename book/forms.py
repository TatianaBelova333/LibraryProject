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


'''
    def __init__(self, *args, **kwargs):
        """Override borrowed_books field for the Reader model.
        Return books that are on the reader's hands or/and available in the library."""
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            queryset = Book.objects.filter(amount__gt=0) | self.instance.borrowed_books.all()
        else:
            queryset = Book.objects.filter(amount__gt=0)
        self.fields['borrowed_books'].queryset = queryset.distinct()
'''


"""
    def save(self, commit=True):
        instance = super().save(commit=False)
        print(instance.id)
        print(self.cleaned_data.get('borrowed_books'))
        books_wanted = self.cleaned_data.get('borrowed_books')
        print(instance.borrowed_books.all())
        if instance.pk:
            previously_borrowed_books = set(instance.borrowed_books.all())
            new_books = books_wanted.difference(previously_borrowed_books)
            returned_books = previously_borrowed_books.difference(books_wanted)
            if new_books:
                for book in new_books:
                    instance.borrowed_books.add(book)
                    book = Book.objects.get(pk=book.pk)
                    book.amount -= 1
                    book.save()
            if returned_books:
                for book in returned_books:
                    instance.borrowed_books.remove(book)
                    book = Book.objects.get(pk=book.pk)
                    book.amount += 1
                    book.save()
        else:
            instance = Reader.objects.create(**self.cleaned_data)
            print(instance)
            for book in books_wanted:
                instance.borrowed_books.add(book)
                book = Book.objects.get(pk=book.pk)
                book.amount -= 1
                book.save()
        return instance
"""