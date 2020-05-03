"""Users app models."""
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Table for `user` that subclass `AbstractUser`."""

    email = models.EmailField(max_length=100, unique=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
