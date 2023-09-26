from .models import Record
from .serializers import RecordSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# from api.permissions import IsStaffEditorPermissions
# from api.mixins import StaffEditorPermissionMixin
from typing import Any

class RecordListAPIView(APIView):
    def get(self, request, format=None):
        record = Record.objects.all()
        serializer = RecordSerializer(record, many=True)
        return Response(serializer.data)
    
record_list_view: Any = RecordListAPIView.as_view()

