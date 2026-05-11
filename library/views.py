from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import Book, BorrowRecord

def home(request):
    return render(request, 'home.html')

def cover(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'logIN.html')

def signup(request):
    return render(request, 'signup.html')

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def admin_books(request):
    return render(request, 'admin_available_books.html')

def add_book(request):
    return render(request, 'Add_Book.html')

def edit_book(request):
    return render(request, 'Edit_Book.html')

def borrowed_books(request):
    return render(request, 'borrowed-books.html')

def book_details(request):
    return render(request, 'book-details.html')

def checkout(request):
    return render(request, 'checkout.html')


def login_view(request):
    """Handle actual login logic (POST request)"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_admin = request.POST.get('role') == 'true'
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if is_admin == (user.is_superuser or user.is_staff):
                auth_login(request, user)
                if user.is_superuser or user.is_staff:
                    return redirect('admin_dashboard')
                else:
                    return redirect('cover')
            else:
                messages.error(request, 'Invalid role selected')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'logIN.html')


def signup_view(request):
    """Handle actual signup logic (POST request)"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_admin = request.POST.get('Is_Admin') == 'true'
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'signup.html')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        if is_admin:
            user.is_staff = True
            user.save()
        
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')
    
    return render(request, 'signup.html')


def cart(request):
    return render(request, 'cart.html')

def logout_view(request):
    from django.contrib.auth import logout as auth_logout
    auth_logout(request)
    return redirect('cover')

def api_stats(request):
    from django.http import JsonResponse
    from .models import Book
    from django.contrib.auth.models import User
    return JsonResponse({
        'total_books': Book.objects.count(),
        'total_users': User.objects.count(),
    })
