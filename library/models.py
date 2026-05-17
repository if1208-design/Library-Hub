from django.db import models
from django.conf import settings


class Book(models.Model):

    CATEGORY_CHOICES = [
        ('fiction', 'Fiction'),
        ('psychology', 'Psychology & Self-help'),
        ('science', 'Science & Productivity'),
        ('history', 'History & Religion'),
        ('technology', 'Technology'),
        ('literature', 'Literature'),
        ('children', 'Children'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)

    author = models.CharField(max_length=255)

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default='other'
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    cover_image = models.ImageField(
        upload_to='covers/',
        blank=True,
        null=True
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00
    )

    borrow_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00
    )

    total_copies = models.PositiveIntegerField(
        default=1
    )

    available_copies = models.PositiveIntegerField(
        default=1
    )

    added_date = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.title} by {self.author}"

    def is_available(self):
        return self.available_copies > 0
    
    isEbook = models.BooleanField(default=False, verbose_name= "E-book Available")
    ebookFile = models.FileField(upload_to='ebooks/',null=True,blank=True, verbose_name= "E-book File")#null for db and blank for forms
    def ebookAvailable(self):
            return bool(self.ebookFile)




class BorrowRecord(models.Model):

    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='borrow_records'
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='borrow_records'
    )

    borrow_date = models.DateField(
        auto_now_add=True
    )

    due_date = models.DateField()

    return_date = models.DateField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='borrowed'
    )

    def __str__(self):
        return f"{self.user.username} -> {self.book.title} ({self.status})"

    def is_overdue(self):

        from datetime import date

        return (
            self.status == 'borrowed'
            and self.due_date < date.today()
        )