from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from book.models import Author, Book, Reader


class AuthorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        read_only_fields = ["id", "created", "updated"]
        fields = "__all__"


class AuthorDetailSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%d.%m.%Y")
    updated = serializers.DateTimeField(format="%d.%m.%Y")

    class Meta:
        model = Author
        read_only_fields = ["id", "created", "updated"]
        fields = ('pk', 'full_name', "photo", "created", "updated")


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        read_only_fields = ["id", "created", "updated"]
        fields = '__all__'


class BookDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.full_name')
    created = serializers.DateTimeField(format="%d.%m.%Y")
    updated = serializers.DateTimeField(format="%d.%m.%Y")

    class Meta:
        model = Book
        read_only_fields = ["id", "created", "updated"]
        fields = '__all__'


class ReaderDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='full_name')
    borrowed_books = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title',
        many=True,
    )

    class Meta:
        model = Reader
        read_only_fields = ["id", "created", "updated"]
        fields = (
            'id',
            'username',
            'name',
            'phone_number',
            'is_active',
            'is_staff',
            'borrowed_books',
        )


class ReaderCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    borrowed_books = serializers.SlugRelatedField(
        required=False,
        slug_field='title',
        many=True,
        queryset=Book.objects.filter(amount__gt=0),
    )

    class Meta:
        model = Reader
        read_only_fields = ["created", "updated"]
        fields = (
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'is_active',
            'password',
            'borrowed_books',
    )

    def validate_borrowed_books(self, value):
        max_book_count = 3
        if value and len(value) > max_book_count:
            raise ValidationError('Читатель может взять не больше 3 книг.')
        for book in value:
            if book in Book.objects.filter(amount=0):
                raise ValidationError(f'{book} нет в наличии.')
        return value

    def create(self, validated_data):
        borrowed_books = validated_data.pop('borrowed_books', None)
        reader = Reader.objects.create(**validated_data)
        reader.set_password(validated_data["password"])
        if borrowed_books:
            for book in borrowed_books:
                reader.borrowed_books.add(book)
                book = Book.objects.get(pk=book.pk)
                book.amount -= 1
                book.save()
        reader.save()
        return reader


class ReaderUpdateSerializer(serializers.ModelSerializer):
    borrowed_books = serializers.SlugRelatedField(
        required=False,
        slug_field='title',
        many=True,
        queryset=Book.objects.all(),
    )
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Reader
        read_only_fields = ["id", "created", "updated"]
        exclude = ('email', 'date_joined', 'last_login', 'groups', 'user_permissions')

    def validate_borrowed_books(self, value):
        max_book_count = 3
        if value and len(value) > max_book_count:
            raise ValidationError('Читатель может взять не больше 3 книг.')
        for book in value:
            if book in Book.objects.filter(amount=0):
                raise ValidationError(f'{book} нет в наличии.')
        return value

    def update(self, instance, validated_data):
        books_wanted = validated_data.pop('borrowed_books', None)
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        if books_wanted:
            books_wanted = set(books_wanted)
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
            instance.save()
        super().update(instance, validated_data)
        return instance
