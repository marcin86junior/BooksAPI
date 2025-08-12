from django.urls import path, re_path
from books.views import BookViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Library API",
        default_version='v1',
        description="API for managing books in the library",
        contact=openapi.Contact(email="contact@yourdomain.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

borrow_book = BookViewSet.as_view({'post': 'borrow'})
return_book = BookViewSet.as_view({'post': 'return_book'})

urlpatterns = [
    path('books/', BookViewSet.as_view({'get': 'list', 'post': 'create'}), name='book-list'),
    path('books/<str:serial_number>/', BookViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='book-detail'),
    path('books/<str:serial_number>/borrow/<str:person_id>/', borrow_book, name='book-borrow'),
    path('books/<str:serial_number>/return_book/<str:person_id>/', return_book, name='book-return'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
