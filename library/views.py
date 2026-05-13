from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User  # Using standard auth model to match teammate's setup
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import models
from .models import Book, BorrowRecord

# --- Base Application Page Templates Navigation ---

def home(request):
    return render(request, 'home.html')


def cover(request):
    return render(request, 'index.html')


def admin_books(request):
    return render(request, 'admin_available_books.html')


def borrowed_books(request):
    return render(request, 'borrowed-books.html')


def book_details(request):
    return render(request, 'book-details.html')


def checkout(request):
    return render(request, 'checkout.html')


def cart(request):
    return render(request, 'cart.html')


# --- Core User Management Authentication Processes ---

def login_view(request):
    """Handles login authentication checks using built-in staff/superuser flags."""
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
    
    return render(request, 'authentication/logIN.html')


def signup_view(request):
    """Creates database user entries and assigns staff status to administrators."""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_admin = request.POST.get('Is_Admin') == 'true'
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'authentication/signup.html')
        
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
    
    return render(request, 'authentication/signup.html')


def logout_view(request):
    auth_logout(request)
    return redirect('cover')


# --- Core Dashboard Analytics Views (Database Migrated) ---

@login_required
def admin_dashboard(request):
    """Renders the dashboard metrics panel by reading live data directly out of SQLite."""
    # Authenticate via teammate's user model permission syntax rule
    if not (request.user.is_staff or request.user.is_superuser):
        return render(request, 'authentication/logIN.html', {'error': 'Access denied! Admin permissions required.'})
        
    # Calculate counters dynamically using teammate's copy attributes schema
    total_books = Book.objects.aggregate(total=models.Sum('total_copies'))['total'] or 0
    available_books = Book.objects.aggregate(available=models.Sum('available_copies'))['available'] or 0
    borrowed_count = max(0, total_books - available_books)
    user_count = User.objects.filter(is_staff=False, is_superuser=False).count()

    context = {
        'total_books': total_books,
        'borrowed_count': borrowed_count,
        'available_count': available_books,
        'user_count': user_count,
    }
    return render(request, 'admin_dashboard.html', context)


# --- Library Book CRUD Management Operations ---

def add_book(request):
    if request.method == 'POST':
        title      = request.POST.get('book_name')
        author     = request.POST.get('author')
        category   = request.POST.get('category')
        desc       = request.POST.get('description')
        copies     = int(request.POST.get('total_copies', 1))
        price      = request.POST.get('price', 0)
        borrow_fee = request.POST.get('borrow_fee', 0)
        image      = request.FILES.get('cover_image')

        Book.objects.create(
            title            = title,
            author           = author,
            category         = category,
            description      = desc,
            total_copies     = copies,
            available_copies = copies,  
            price            = price,
            borrow_fee       = borrow_fee,
            cover_image      = image,
        )
        messages.success(request, f'"{title}" added successfully!')
        return redirect('admin_books')

    return render(request, 'Add_Book.html')


def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.title       = request.POST.get('book_name')
        book.author      = request.POST.get('author')
        book.category    = request.POST.get('category')
        book.description = request.POST.get('description')
        book.price       = request.POST.get('price', 0)
        book.borrow_fee  = request.POST.get('borrow_fee', 0)

        new_total             = int(request.POST.get('total_copies', book.total_copies))
        diff                  = new_total - book.total_copies
        book.total_copies     = new_total
        book.available_copies = max(0, book.available_copies + diff)

        if request.FILES.get('cover_image'):
            book.cover_image = request.FILES['cover_image']

        book.save()
        messages.success(request, f'"{book.title}" updated!')
        return redirect('admin_books')

    return render(request, 'Edit_Book.html', {'book': book})


# --- Dynamic AJAX Backend Database JSON Endpoints ---

@login_required
def api_books_list(request):
    """API endpoint to feed search entries directly from models to frontend template calls."""
    if not (request.user.is_staff or request.user.is_superuser):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    query = request.GET.get('search', '').strip()
    books = Book.objects.all()

    if query:
        books = books.filter(
            models.Q(title__icontains=query) |
            models.Q(author__icontains=query) |
            models.Q(category__icontains=query)
        )

    books_data = []
    for book in books:
        # Determine borrow state flags dynamically via inventory volume differences
        is_borrowed_out = book.available_copies == 0
        
        books_data.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'category': book.category,
            'is_borrowed': is_borrowed_out,
        })

    return JsonResponse({'books': books_data})


@login_required
def delete_book(request, book_id):
    """Removes targeted primary record rows seamlessly out of database model layers."""
    if not (request.user.is_staff or request.user.is_superuser):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        book.delete()
        return JsonResponse({'success': True, 'message': 'Book deleted successfully.'})
        
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def api_stats(request):
    """Teammate's secondary quick statistic summary endpoint API tracking numbers."""
    return JsonResponse({
        'total_books': Book.objects.count(),
        'total_users': User.objects.count(),
    })