from .models import Record
from .serializers import RecordSerializer, CreateRecordSerializer
from rest_framework import generics
from rest_framework import permissions
from typing import Any
from medicalapp.common.pydantic_models import URLParams, CreateRecordRequest, UpdateRecordRequest, APIResponseModel
from rest_framework import exceptions
from rest_framework.response import Response

class RecordListAPIView(generics.ListAPIView):
    queryset: Record = Record.objects.all()
    serializer_class: Any = RecordSerializer
    permission_classes: Any = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return Record.objects.filter(patient=self.request.user).all()
    
record_list_view: Any = RecordListAPIView.as_view()
    
class RecordCreateAPIView(generics.CreateAPIView):
    # queryset: Record = Record.objects.all()
    serializer_class: Any = CreateRecordSerializer
    permission_classes: Any = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def perform_create(self, serializer):
        CreateRecordRequest.model_validate(self.request.data)
        if self.request.user.is_staff:
            serializer.validated_data
            serializer.save()
        else:
            raise exceptions.PermissionDenied
        

record_create_view: Any = RecordCreateAPIView.as_view()


class RecordDetailAPIView(generics.RetrieveAPIView):
    queryset: Record = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        urlparam: dict = URLParams.model_validate(self.kwargs).model_dump()
        if self.request.user.is_staff:
            return super().get_queryset()
        return (
            Record.objects.filter(patient=self.request.user)
            .filter(pk=urlparam.get("pk"))
            .all()
        )


record_detail_view: Any = RecordDetailAPIView.as_view()


class RecordUpdateAPIView(generics.UpdateAPIView):
    queryset: Record = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    lookup_field = "pk"

    def perform_update(self, serializer):
        UpdateRecordRequest.model_validate(self.request.data)
        serializer.validated_data
        serializer.save()
        return "snnnshhhshshs"


record_update_view = RecordUpdateAPIView.as_view()


class RecordDestroyAPIView(generics.DestroyAPIView):
    queryset: Record = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    lookup_field = "pk"

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


record_delete_view = RecordDestroyAPIView.as_view()
