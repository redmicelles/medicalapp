# Create your views here.
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .helpers.token import get_tokens_for_user
from .serializers import RegistrationSerializer, PasswordChangeSerializer
from rest_framework_simplejwt import views as jwt_views
from medicalapp.common.pydantic_models import (
    CreateUserRequest,
    LoginRequest,
    APIResponseModel,
    APIErrorModel,
)
from typing import Any


class RegistrationView(APIView):
    def post(self, request: dict) -> dict:
        CreateUserRequest.model_validate(self.request.data)
        serializer: Any = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = APIResponseModel.model_validate({"data": serializer.data})
            return Response(
                response_data,
                status=status.HTTP_201_CREATED,
            )
        error_data: dict = APIErrorModel.model_validate({"error": serializer.errors})
        return Response(error_data, status=status.HTTP_400_BAD_REQUEST)


register_view: Any = RegistrationView.as_view()


class LoginView(APIView):
    def post(self, request: dict) -> dict:
        LoginRequest.model_validate(request.data)
        email: str = request.data.get("email")
        password: str = request.data.get("password")
        user: Any = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            auth_data: dict = get_tokens_for_user(request.user)
            return Response(
                APIResponseModel.model_validate({"data": auth_data}),
                status=status.HTTP_200_OK,
            )
        error_data: dict = APIErrorModel.model_validate(
            {"error": {"message": "Invalid authentication credential(s)!"}}
        )
        return Response(error_data, status=status.HTTP_400_BAD_REQUEST)


login_view: Any = LoginView.as_view()


class LogoutView(APIView):
    def post(self, request: dict) -> dict:
        logout(request)
        return Response(
            APIResponseModel.model_validate(
                {"data": {"message": "Successfully logged out"}}
            ),
            status=status.HTTP_200_OK,
        )


logout_view: Any = LogoutView.as_view()


class ChangePasswordView(APIView):
    permission_classes: list = [
        IsAuthenticated,
    ]

    def post(self, request: dict) -> None:
        serializer = PasswordChangeSerializer(
            context={"request": request}, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


change_password_view: Any = ChangePasswordView.as_view()

refresh_token_view: Any = jwt_views.TokenRefreshView.as_view()
