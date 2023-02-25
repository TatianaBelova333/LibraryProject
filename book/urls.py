from django.urls import path, include
from rest_framework.routers import SimpleRouter

from book.views import AuthorViewSet, BookViewSet, ReaderViewSet

app_name = 'book'

author_router = SimpleRouter()
author_router.register(r'authors', AuthorViewSet, basename="authors")

book_router = SimpleRouter()
book_router.register(r'books', BookViewSet, basename="books")

reader_router = SimpleRouter()
book_router.register(r'readers', ReaderViewSet, basename="readers")

urlpatterns = [
    path("", include(author_router.urls)),
    path("", include(book_router.urls)),
    path("", include(reader_router.urls)),
]
