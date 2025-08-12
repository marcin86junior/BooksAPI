from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, data):
        status_value = data.get('status') or getattr(self.instance, 'status', None)

        if status_value == 'borrowed':
            borrower = data.get('borrowed_by') or getattr(self.instance, 'borrowed_by', None)
            if not borrower:
                raise serializers.ValidationError({'borrowed_by': 'Required when the status is "borrowed".'})
        elif status_value == 'available':
            data['borrowed_by'] = None
            data['borrowed_at'] = None

        return data
