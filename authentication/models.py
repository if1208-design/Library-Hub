from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
import random
import datetime


class User(AbstractUser):

    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )

    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class PasswordResetCode(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    code = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)

    def is_expired(self):
        expiry_time = self.created_at + datetime.timedelta(minutes=15)
        return timezone.now() > expiry_time

    def __str__(self):
        return f"Reset code for {self.user.username}"
