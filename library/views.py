from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Book


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

def borrowed_books(request):
    return render(request, 'borrowed-books.html')

def book_details(request):
    return render(request, 'book-details.html')

def checkout(request):
    return render(request, 'checkout.html')


def add_book(request):
    if request.method == 'POST':
        
        title      = request.POST.get('book_name')
        author     = request.POST.get('author')
        category   = request.POST.get('category')
        desc       = request.POST.get('description')
        copies     = request.POST.get('total_copies', 1)
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

    # GET — send book data to pre-fill the form
    return render(request, 'Edit_Book.html', {'book': book})
