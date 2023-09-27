import logging
from rest_framework.views import exception_handler
from django.http import JsonResponse
from rest_framework import status
import traceback
from .logger import logging
from rest_framework_simplejwt import exceptions as jwt_exceptions
from django.http.response import Http404
from rest_framework import exceptions as drf_exceptions
from pydantic import ValidationError


def global_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, Http404):
        err_message = {"error": {"message": str(exc)}}
        return JsonResponse(err_message, safe=False, status=400)
    if isinstance(exc, TypeError):
        err_message = {"error": {"message": str(exc)}}
        return JsonResponse(err_message, safe=False, status=400)
    if isinstance(exc, ValidationError):
        errors = exc.errors()[0]
        errors.pop("url")
        err_message = {"error": {"message": errors}}
        return JsonResponse(err_message, safe=False, status=422)
    if isinstance(exc, jwt_exceptions.InvalidToken):
        err_message = {"error": {"message": "Invalid token presented!"}}
        return JsonResponse(err_message, safe=False, status=401)
    # if isinstance(exc, drf_exceptions.ValidationError):
    #     err_message = {"error": {"message": str(exc)}}
    #     return JsonResponse(err_message, safe=False, status=400)
    if isinstance(exc, drf_exceptions.NotAuthenticated):
        err_message = {"error": {"message": str(exc)}}
        return JsonResponse(err_message, safe=False, status=403)
    if isinstance(exc, drf_exceptions.PermissionDenied):
        err_message = {"error": {"message": str(exc)}}
        return JsonResponse(err_message, safe=False, status=403)
    if isinstance(exc, drf_exceptions.APIException):
        return JsonResponse({"error": {"message": exc.detail.get("message")}}, safe=False, status=exc.detail.get("status"))
    if isinstance(exc, Exception):
        err_message = (
            {
                "error": {
                    "message": "We've just hit a snag! We've noted this and will address it shortly!!"
                }
            },
        )
        logging.error(f"Internal Server Error!!!: {traceback.format_exc()}")
        return JsonResponse(
            err_message[0], safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return response


class CustomErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            return JsonResponse(
                {
                    "error": {
                        "message": "It appears we do not have the resource(s) you have requested."
                    }
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if response.status_code == 403:
            return JsonResponse(
                {
                    "error": {
                        "message": "You do not have permission to perform this action"
                    }
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # if response.status_code == 401:
        #     return JsonResponse(
        #         {"error": {"message": "Authentication failed!"}},
        #         status=status.HTTP_401_UNAUTHORIZED,
        #     )

        if str(response.status_code).startswith("5"):
            logging.error(f"Internal Server Error!!!: {str(response)}")
            return JsonResponse(
                {
                    "error": {
                        "message": "We've just hit a snag! We've noted this and will address it shortly!!"
                    }
                },
                status=status.HTTP_501_NOT_IMPLEMENTED,
            )
        return response
