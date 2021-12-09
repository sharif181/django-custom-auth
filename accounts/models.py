from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomAccountManager(BaseUserManager):
    """Custom User manager for creating user"""

    def create_superuser(self, email, username, password, **othersField):
        othersField.setdefault('is_superuser', True)
        othersField.setdefault('is_staff', True)
        othersField.setdefault('is_active', True)

        if othersField.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')

        if othersField.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')

        return self.create_user(email, username, password, **othersField)

    def create_user(self, email, username, password, **othersField):
        if not email:
            raise ValueError(_('you must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **othersField)
        user.set_password(password)
        user.save()
        return user


# Custom authentication model
class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=50, unique=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.username)
