from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager
from typing import Any

# Create your models here.
class CustomUser(AbstractUser):
    username: Any = None
    email: Any = models.EmailField(verbose_name="email address", unique=True)
    full_name: Any = models.CharField(max_length=255)
    is_active: Any = models.BooleanField(default=True)
    is_admin: Any = models.BooleanField(default=False)

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: str = ('full_name', )
    objects: Any = CustomUserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
