from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import models
from datetime import date, timedelta

from .models import Book, BorrowRecord


def home(request):
    return render(request, 'home.html')


def cover(request):
    books_by_category = {}
    for code, label in Book.CATEGORY_CHOICES:
        books = Book.objects.filter(category=code)
        if books.exists():
            books_by_category[label] = books
    return render(request, 'index.html', {'books_by_category': books_by_category})


def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


def admin_books(request):
    return redirect('cover')


def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    already_borrowed = False
    if request.user.is_authenticated:
        already_borrowed = BorrowRecord.objects.filter(
            user=request.user, book=book, status='borrowed'
        ).exists()
    return render(request, 'book-details.html', {
        'book': book,
        'already_borrowed': already_borrowed,
    })


def checkout(request):
    return render(request, 'checkout.html')


def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('book_name')
        author = request.POST.get('author')
        category = request.POST.get('category')
        desc = request.POST.get('description')
        copies = int(request.POST.get('total_copies', 1))
        price = request.POST.get('price', 0)
        borrow_fee = request.POST.get('borrow_fee', 0)
        image = request.FILES.get('cover_image')

        Book.objects.create(
            title=title,
            author=author,
            category=category,
            description=desc,
            total_copies=copies,
            available_copies=copies,
            price=price,
            borrow_fee=borrow_fee,
            cover_image=image,
        )
        messages.success(request, f'"{title}" added successfully!')
        return redirect('admin_dashboard')

    return render(request, 'Add_Book.html')


def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.title = request.POST.get('book_name')
        book.author = request.POST.get('author')
        book.category = request.POST.get('category')
        book.description = request.POST.get('description')
        book.price = request.POST.get('price', 0)
        book.borrow_fee = request.POST.get('borrow_fee', 0)

        new_total = int(request.POST.get('total_copies', book.total_copies))
        diff = new_total - book.total_copies
        book.total_copies = new_total
        book.available_copies = max(0, book.available_copies + diff)

        if request.FILES.get('cover_image'):
            book.cover_image = request.FILES['cover_image']

        book.save()
        messages.success(request, f'"{book.title}" updated!')
        return redirect('admin_dashboard')

    return render(request, 'Edit_Book.html', {'book': book})


def login_view(request):
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
            user.is_superuser = True
            user.save()

        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')

    return render(request, 'authentication/signup.html')


def cart(request):
    return render(request, 'cart.html')


def logout_view(request):
    auth_logout(request)
    return redirect('cover')


def api_stats(request):
    return JsonResponse({
        'total_books': Book.objects.count(),
        'total_users': User.objects.count(),
    })


@login_required
def api_books_list(request):
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
        books_data.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'category': book.category,
            'is_borrowed': book.available_copies == 0,
        })

    return JsonResponse({'books': books_data})


@login_required
def delete_book(request, book_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        book.delete()
        return JsonResponse({'success': True, 'message': 'Book deleted successfully.'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def borrow_book(request, pk):
    if request.method != 'POST':
        return redirect('book_details', pk=pk)
    book = get_object_or_404(Book, pk=pk)
    if BorrowRecord.objects.filter(user=request.user, book=book, status='borrowed').exists():
        messages.warning(request, f'You already borrowed "{book.title}".')
        return redirect('book_details', pk=pk)
    if not book.is_available():
        messages.error(request, f'No copies available for "{book.title}".')
        return redirect('book_details', pk=pk)
    BorrowRecord.objects.create(
        user=request.user, book=book,
        due_date=date.today() + timedelta(days=14),
        status='borrowed',
    )
    book.available_copies -= 1
    book.save(update_fields=['available_copies'])
    messages.success(request, f'You borrowed "{book.title}"!')
    return redirect('borrowed_books')


@login_required
def return_book(request, record_id):
    if request.method != 'POST':
        return redirect('borrowed_books')
    record = get_object_or_404(BorrowRecord, pk=record_id, user=request.user)
    if record.status == 'returned':
        messages.info(request, 'Already returned.')
        return redirect('borrowed_books')
    record.status = 'returned'
    record.return_date = date.today()
    record.save(update_fields=['status', 'return_date'])
    record.book.available_copies += 1
    record.book.save(update_fields=['available_copies'])
    messages.success(request, f'"{record.book.title}" returned!')
    return redirect('borrowed_books')


@login_required
def borrowed_books(request):
    active = BorrowRecord.objects.filter(user=request.user, status='borrowed').select_related('book')
    returned = BorrowRecord.objects.filter(user=request.user, status='returned').select_related('book')
    return render(request, 'borrowed-books.html', {
        'active_records': active,
        'returned_records': returned,
        'today': date.today(),
    })
