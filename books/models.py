from django.db import models
from django.core.validators import RegexValidator

six_digits = RegexValidator(r'^\d{6}$', 'Must be exactly 6 digits')


class Book(models.Model):
    STATUS_TYPES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
    ]

    serial_number = models.CharField(max_length=6, primary_key=True, validators=[six_digits])
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_TYPES, default='available')

    borrowed_by = models.CharField(max_length=6, blank=True, null=True, validators=[six_digits])
    borrowed_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.serial_number} — {self.title} ({self.get_status_display()})"
