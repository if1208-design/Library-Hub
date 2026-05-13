from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Book, BorrowRecord
from django.http import HttpResponse
from django.http import Http404,FileResponse


def home(request):
    return render(request, 'home.html')


def cover(request):
    # get search query and the search filter from the URL
    query = request.GET.get('q', '').strip()
    search_filter = request.GET.get('search_filter', 'title') # default search by title
    
    # get all books initially
    books = Book.objects.all()
    
    if query:
        if search_filter == 'title':
            books = books.filter(title__icontains=query) # -contains is case insensitive
        elif search_filter == 'author':
            books = books.filter(author__icontains=query)
        elif search_filter == 'category':
            matching_keys = [
                key for key, label in Book.CATEGORY_CHOICES 
                if query.lower() in label.lower() or query.lower() in key.lower()
            ]
            books = books.filter(category__in=matching_keys)
    # Debug print
    print(f"Search query: '{query}'")
    print(f"Search filter: {search_filter}")
    print(f"Number of books found: {books.count()}")
    for book in books:
        print(f"  - {book.title}")

    categories = {}
    for book in books:
        cat_name = dict(Book.CATEGORY_CHOICES).get(book.category, book.category)
        if cat_name not in categories:
            categories[cat_name] = []
        categories[cat_name].append(book)
        

    filtered_results = {
        'books': books,
        'query': query if query else None, # Ensures empty input registers as no query active
        'searchFilter': search_filter,
        'categories': categories, 
    }
    return render(request, 'index.html', filtered_results)


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

    return render(request, 'Edit_Book.html', {'book': book})


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
    
    return render(request, 'authentication/logIN.html')


def signup_view(request):
    """Handle actual signup logic (POST request)"""
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
def ebook(request, book_id):
    from django.shortcuts import get_object_or_404
    book = get_object_or_404(Book, id= book_id)
    if not book.ebookAvailable():
        raise Http404("E-book not available")
    return FileResponse( book.ebookFile, content_type='application/pdf', filename=f"{book.title}.pdf")