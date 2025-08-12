from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from books.models import Book


class BookAPITests(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(
            serial_number='123456',
            title='Testowa Książka',
            author='Jan Kowalski',
            status='available'
        )

    def test_books_list(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_books_create(self):
        url = reverse('book-list')
        data = {
            'serial_number': '654321',
            'title': 'Nowa Książka',
            'author': 'Anna Nowak',
            'status': 'available'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['serial_number'], data['serial_number'])

    def test_books_read(self):
        url = reverse('book-detail', kwargs={'serial_number': self.book.serial_number})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['serial_number'], self.book.serial_number)

    def test_books_delete(self):
        url = reverse('book-detail', kwargs={'serial_number': self.book.serial_number})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(serial_number=self.book.serial_number).exists())

    def test_books_borrow(self):
        url = reverse('book-borrow', kwargs={
            'serial_number': self.book.serial_number,
            'person_id': '111111'
        })
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, 'borrowed')
        self.assertEqual(self.book.borrowed_by, '111111')

    def test_books_borrow_already_borrowed(self):
        self.book.status = 'borrowed'
        self.book.borrowed_by = '222222'
        self.book.save()
        url = reverse('book-borrow', kwargs={
            'serial_number': self.book.serial_number,
            'person_id': '111111'
        })
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_books_return_book(self):
        self.book.status = 'borrowed'
        self.book.borrowed_by = '111111'
        self.book.borrowed_at = '2025-08-11T11:28:46Z'
        self.book.save()

        url = reverse('book-return', kwargs={
            'serial_number': self.book.serial_number,
            'person_id': '111111'
        })
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, 'available')
        self.assertIsNone(self.book.borrowed_by)
        self.assertIsNone(self.book.borrowed_at)

    def test_books_return_book_not_borrowed(self):
        url = reverse('book-return', kwargs={
            'serial_number': self.book.serial_number,
            'person_id': '111111'
        })
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
