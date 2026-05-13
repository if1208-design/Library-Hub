from django.urls import path
from . import views

urlpatterns = [
    # --- Authentication Paths ---
    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'signup/',
        views.signup,
        name='signup'
    ),

    # Step 1: request the code by email
    path(
        'reset-password/request/',
        views.request_reset_code,
        name='request_reset_code'
    ),

    # Step 2: submit the code and new password
    path(
        'reset-password/',
        views.reset_password,
        name='reset_password'
    ),

    path(
        'dashboard/', 
        views.admin_dashboard, 
        name='admin_dashboard'
    ),
    
    path(
        'api/books/', 
        views.api_books_list, 
        name='api_books_list'
    ),
    
    path(
        'api/books/delete/<int:book_id>/', 
        views.delete_book, 
        name='delete_book'
    ),
]