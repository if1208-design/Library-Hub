from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cover/', views.cover, name='cover'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-books/', views.admin_books, name='admin_books'),
    path('add-book/',views.add_book, name='add_book'),
    path('edit-book/<int:pk>/', views.edit_book,name='edit_book'),
    path('borrowed-books/', views.borrowed_books, name='borrowed_books'),  # ← أضف
    path('book-details/', views.book_details, name='book_details'),        # ← أضف
    path('checkout/', views.checkout, name='checkout'),                    # ← أضف
]