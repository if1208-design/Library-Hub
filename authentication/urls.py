from django.urls import path
from . import views

urlpatterns = [
    # --- Authentication Paths Only ---
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
]