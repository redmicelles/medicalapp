from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager
from typing import Any


# Create your models here.
class CustomUser(AbstractUser):
    username: Any = None
    email: Any = models.EmailField(verbose_name="email address", unique=True)
    other_names: Any = models.CharField(max_length=100)
    surname: Any = models.CharField(max_length=50)
    date_of_birth: Any = models.DateField()
    is_active: Any = models.BooleanField(default=True)
    is_admin: Any = models.BooleanField(default=False)

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: str = ("surname", "other_names", "date_of_birth")
    objects: Any = CustomUserManager()

    def __str__(self) -> Any:
        return self.email

    def has_perm(self, perm, obj=None) -> bool:
        return True

    def has_module_perms(self, app_label) -> bool:
        return True

    @property
    def is_staff(self) -> Any:
        return self.is_admin
