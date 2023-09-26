from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms
from .models import CustomUser
from typing import Any, Union


class UserCreationForm(forms.ModelForm):
    password1: Any = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2: Any = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model: Any = CustomUser
        fields: tuple = ("email", "surname", "other_names", "date_of_birth")

    def clean_password2(self):
        password1: str = self.cleaned_data.get("password1")
        password2: str = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords Mismatch")
        return password2

    def save(self, commit=True):
        user: Any = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model: Any = CustomUser
        fields: tuple = (
            "email",
            "password",
            "other_names",
            "surname",
            "date_of_birth",
            "is_active",
        )

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form: Any = UserChangeForm
    add_form: Any = UserCreationForm
    list_display: tuple = (
        "email",
        "other_names",
        "surname",
        "date_of_birth",
        "is_admin",
    )
    list_filter: tuple = ("is_admin",)
    fieldsets: tuple = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("other_names", "surname", "date_of_birth")}),
        ("Permissions", {"fields": ("is_admin",)}),
    )
    add_fieldsets: tuple = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "other_names",
                    "surname",
                    "date_of_birth",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields: tuple = ("email",)
    ordering: tuple = ("email",)
    filter_horizontal: Union[tuple, None] = ()


admin.site.register(CustomUser, UserAdmin)
