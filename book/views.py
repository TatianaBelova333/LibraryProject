from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

from book.models import Author, Book, Reader
from book.serializers import (BookDetailSerializer, BookCreateSerializer, AuthorDetailSerializer,
                              AuthorCreateSerializer, ReaderDetailSerializer, ReaderCreateSerializer,
                              ReaderUpdateSerializer)


class IsAdminOrReader(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or obj == request.user:
            return True
        return False


class AuthorViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing author instances.

    """
    serializer_class = AuthorDetailSerializer
    queryset = Author.objects.all()

    def get_permissions(self):
        """Instantiates and returns the list of permissions that this view requires."""

        if self.action in ('retrieve', 'list'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

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

    def get_permissions(self):
        """Instantiates and returns the list of permissions that this view requires."""
        if self.action in ('retrieve', 'list'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

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

    def get_permissions(self):
        """Instantiates and returns the list of permissions that this view requires."""
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ('update', 'destroy', 'partial_update', 'retrieve', 'list'):
            permission_classes = [IsAuthenticated, IsAdminOrReader]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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
