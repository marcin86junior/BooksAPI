from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Book
from .serializers import BookSerializer
import re


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('serial_number')
    lookup_field = 'serial_number'

    def get_serializer_class(self):
        if self.action in ['borrow', 'return_book']:
            return None
        return BookSerializer

    @action(detail=True, methods=['post'], url_path=r'borrow/(?P<person_id>\d{6})')
    def borrow(self, request, serial_number=None, person_id=None):
        book = self.get_object()

        if book.status == 'borrowed':
            return Response({'detail': 'The book is already borrowed'}, status=status.HTTP_400_BAD_REQUEST)

        if not re.match(r'^\d{6}$', person_id):
            return Response({'detail': 'Person ID must be exactly 6 digits.'}, status=status.HTTP_400_BAD_REQUEST)

        book.status = 'borrowed'
        book.borrowed_by = person_id
        book.borrowed_at = timezone.now()
        book.save()

        return Response(BookSerializer(book).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path=r'return_book/(?P<person_id>\d{6})')
    def return_book(self, request, serial_number=None, person_id=None):
        book = self.get_object()

        if book.status != 'borrowed':
            return Response({'detail': 'The book is not borrowed'}, status=status.HTTP_400_BAD_REQUEST)

        if book.borrowed_by != person_id:
            return Response({'detail': 'Borrower card number does not match'}, status=status.HTTP_400_BAD_REQUEST)

        if not re.match(r'^\d{6}$', person_id):
            return Response({'detail': 'Person ID must be exactly 6 digits.'}, status=status.HTTP_400_BAD_REQUEST)

        book.status = 'available'
        book.borrowed_by = None
        book.borrowed_at = None
        book.save()

        return Response(BookSerializer(book).data, status=status.HTTP_200_OK)
