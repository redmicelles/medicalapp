import logging
from rest_framework.views import exception_handler
from django.http import JsonResponse
from rest_framework import status
import traceback
from .logger import logging
from rest_framework import exceptions
from django.http.response import Http404

def global_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, Http404):
        err_message = {"error": {"message": str(exc)}}
        return JsonResponse(err_message, safe=False, status=400)
    if isinstance(exc, TypeError):
        err_message = {"error": {"message": str(exc)}}
        return JsonResponse(err_message, safe=False, status=400)
    if isinstance(exc, Exception):
        err_message = {"error": {
                "message": "We've just hit a snag! We've noted this and will address it shortly!!"}},
        logging.error(f"Internal Server Error!!!: {traceback.format_exc()}")
        return JsonResponse(err_message[0], safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response

class CustomErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            return JsonResponse({"error": {
                "message": "It appears we do not have the resource(s) you have requested."
            }}, status=status.HTTP_404_NOT_FOUND)
        
        if response.status_code == 403:
            return JsonResponse({"error": {
                "message": "You do not have permission to perform this action"
            }}, status=status.HTTP_403_FORBIDDEN)
        
        if response.status_code == 401:
            return JsonResponse({"error": {
                "message": "Authentication credentials were not provided."
            }}, status=status.HTTP_403_FORBIDDEN)

        return response