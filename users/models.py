from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User model"""
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    image = models.ImageField(upload_to='users_images', null=True, blank=True)
