from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'title', 'author', 'status', 'borrowed_by', 'borrowed_at')
    search_fields = ('serial_number', 'title', 'author', 'borrowed_by')
    list_filter = ('status',)
