from django.db.models import Prefetch
from django.shortcuts import render
from rest_framework import viewsets

from book.models import Author, Book, Reader
from book.serializers import (BookDetailSerializer, BookCreateSerializer, AuthorDetailSerializer,
                              AuthorCreateSerializer, ReaderDetailSerializer, ReaderCreateSerializer,
                              ReaderUpdateSerializer)


class AuthorViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing author instances.
    """
    serializer_class = AuthorDetailSerializer
    queryset = Author.objects.all()

    def get_serializer_class(self):
        """Returns the serializer class for each particular method"""
        if self.action == 'retrieve':
            return AuthorDetailSerializer
        elif self.action in ("create", "partial_update", "update"):
            return AuthorCreateSerializer
        else:
            return AuthorDetailSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing author instances.
    """
    serializer_class = BookDetailSerializer
    queryset = Book.objects.all()

    def get_serializer_class(self):
        """Returns the serializer class for each particular method"""
        if self.action == 'retrieve':
            return BookDetailSerializer
        elif self.action in ("create", "partial_update", "update"):
            return BookCreateSerializer
        else:
            return BookDetailSerializer


class ReaderViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing author instances.
    """
    serializer_class = ReaderDetailSerializer
    queryset = Reader.objects.all()

    def get_serializer_class(self):
        """Returns the serializer class for each particular method"""
        if self.action == 'retrieve':
            return ReaderDetailSerializer
        elif self.action == "create":
            return ReaderCreateSerializer
        elif self.action in ("partial_update", "update"):
            return ReaderUpdateSerializer
        else:
            return ReaderDetailSerializer
