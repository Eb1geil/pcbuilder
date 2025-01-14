from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import ClientManager

class Client(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=25, unique=True)
    address = models.CharField(max_length=100)
    birthday = models.DateField()

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'address', 'birthday', 'phone_number']
    USERNAME_FIELD = 'username'

    objects = ClientManager()

    def __str__(self):
        return self.username
