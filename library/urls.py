from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cover/', views.cover, name='cover'),
    path('logout/', views.logout_view, name='logout_view'),
    
    # Your Dashboard Template View (Using your teammate's path string)
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    path('admin-books/', views.admin_books, name='admin_books'),
    path('add-book/', views.add_book, name='add_book'),
    path('edit-book/<int:pk>/', views.edit_book, name='edit_book'),
    path('borrowed-books/', views.borrowed_books, name='borrowed_books'),
    path('book-details/', views.book_details, name='book_details'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),
    
    # Your Database API Endpoints
    path('api/books/', views.api_books_list, name='api_books_list'),
    path('api/books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('api/stats/', views.api_stats, name='api_stats'),
]