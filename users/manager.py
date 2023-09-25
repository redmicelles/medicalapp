from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email and password are used
    as authentication credentials.
    """

    def create_user(self, email, password, full_name, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
        

    def create_superuser(self, email, password, full_name, **extra_fields):
        user = self.create_user(
            email,
            password=password,
            full_name=full_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user