from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class User(AbstractUser):
    objects = UserManager()
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('agent', 'Manager'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='agent')