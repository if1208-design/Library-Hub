from django.shortcuts import render

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
