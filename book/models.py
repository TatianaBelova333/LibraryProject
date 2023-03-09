from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class DatesModelMixin(models.Model):
    """Abstract class for created/updated db model fields"""

    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата редактирования")

    class Meta:
        abstract = True


class Person(models.Model):
    """Abstract Person model."""
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    middle_name = models.CharField(
        max_length=20,
        verbose_name='Отчество',
        null=True,
        blank=True,
    )
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')

    class Meta:
        abstract = True

    @property
    def full_name(self):
        first_name_initial = f'{self.first_name.upper()[:1]}.'
        if self.middle_name:
            midlle_name_initial = f'{self.middle_name.upper()[:1]}.'
            return f'{self.last_name} {first_name_initial}{midlle_name_initial}'
        return f'{self.last_name} {first_name_initial}'

    def __str__(self) -> str:
        return self.full_name


class Author(Person, DatesModelMixin):
    """Book author model."""
    photo = models.ImageField(
        upload_to='photos/',
        null=True,
        blank=True,
        verbose_name='Фото',
    )

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ('last_name',)


class Book(DatesModelMixin):
    """Book model."""
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    page_count = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(
            limit_value=2,
            message='Кол-во страниц должно быть больше 1.'
        )],
        verbose_name='Количество страниц',
        null=True,
        blank=True,
    )
    author = models.ForeignKey(
        Author,
        verbose_name='Автор',
        related_name='books',
        on_delete=models.SET_NULL,
        null=True,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество книг'
    )

    class Meta:
        unique_together = ('title', 'author')
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ('title', 'author__last_name')

    def __str__(self) -> str:
        return f'{self.title}, {self.author}'


class Reader(Person, DatesModelMixin):
    """Library reader model."""
    phone_number = PhoneNumberField(unique=True, verbose_name='Номер телефона')
    is_active = models.BooleanField(default=True, verbose_name='Статус читателя')
    borrowed_books = models.ManyToManyField(
        Book,
        verbose_name='Активные книги',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'

    def __str__(self) -> str:
        return self.full_name

    def display_borrowed_books(self):
        return '; '.join([str(book) for book in self.borrowed_books.all()])

    display_borrowed_books.short_description = 'Книги на руках'
