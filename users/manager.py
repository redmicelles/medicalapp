from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _
from datetime import date
from typing import Any


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email and password are used
    as authentication credentials.
    """

    def create_user(
        self,
        email: str,
        password: str,
        other_names: str,
        surname: str,
        date_of_birth: date,
    ) -> Any:
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            surname=surname,
            other_names=other_names,
            date_of_birth=date_of_birth,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            email: str,
            password: str,
            other_names: str,
            surname: str,
            date_of_birth: date,
    ) -> Any:
        user = self.create_user(
            email,
            password=password,
            other_names=other_names,
            surname=surname,
            date_of_birth=date_of_birth
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
