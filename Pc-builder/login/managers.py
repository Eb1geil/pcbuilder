from typing import Any
from django.contrib.auth.models import BaseUserManager

class ClientManager(BaseUserManager):
    def create_client(self, email: str, first_name: str, last_name: str, address: str, birthday: str,
                       phone_number: str,  password=None, **extra_fields: Any) -> Any:
        if not first_name:
            raise ValueError('The given username must be set')
        if not last_name:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)

        user = self.model(email=email, first_name=first_name, last_name=last_name,
                           address=address, birthday=birthday, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email='', first_name='', last_name='', address='', birthday='2001-01-01', 
                          phone_number='+375 (37) 537-53-75', password=None, **extra_fields: Any) -> Any:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_client(email, first_name, last_name, address, birthday, phone_number, password, **extra_fields)
        return user