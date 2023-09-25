from rest_framework import serializers
from .models import CustomUser
from typing import Any


class RegistrationSerializer(serializers.ModelSerializer):
    password2: Any = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model: Any = CustomUser
        fields: tuple = ("email", "other_names", "surname", "date_of_birth", "password", "password2")
        extra_kwargs: dict = {"password": {"write_only": True}}

    def save(self) -> Any:
        user: Any = CustomUser(
            email=self.validated_data["email"],
            other_names=self.validated_data["other_names"],
            surname=self.validated_data["surname"],
            date_of_birth=self.validated_data["date_of_birth"],
        )
        password: Any = self.validated_data["password"]
        password2: Any = self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Password mismatch!"})
        user.set_password(password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )
    new_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )

    def validate_current_password(self, value: str) -> str:
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError(
                {"current_password": "Current password does not match"}
            )
        return value
