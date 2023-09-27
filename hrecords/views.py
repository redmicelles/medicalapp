from .models import Record
from .serializers import RecordSerializer, CreateRecordSerializer
from rest_framework import generics
from rest_framework import permissions
from typing import Any
from medicalapp.common.pydantic_models import (
    URLParams,
    CreateRecordRequest,
    UpdateRecordRequest,
)
from rest_framework import exceptions


class RecordListAPIView(generics.ListAPIView):
    queryset: Record = Record.objects.all()
    serializer_class: Any = RecordSerializer
    permission_classes: Any = [permissions.IsAuthenticated]
    lookup_field: str = "pk"

    def get_queryset(self) -> Any:
        if self.request.user.is_staff:
            return super().get_queryset()
        return Record.objects.filter(patient=self.request.user).all()


record_list_view: Any = RecordListAPIView.as_view()


class RecordCreateAPIView(generics.CreateAPIView):
    serializer_class: Any = CreateRecordSerializer
    permission_classes: Any = [permissions.IsAuthenticated]
    lookup_field: str = "pk"

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
    serializer_class: Any = RecordSerializer
    permission_classes: list = [permissions.IsAuthenticated]

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
    serializer_class: Any = RecordSerializer
    permission_classes: list = [permissions.IsAuthenticated, permissions.IsAdminUser]
    lookup_field: Any = "pk"

    def perform_update(self, serializer) -> None:
        UpdateRecordRequest.model_validate(self.request.data)
        serializer.validated_data
        serializer.save()


record_update_view: Any = RecordUpdateAPIView.as_view()


class RecordDestroyAPIView(generics.DestroyAPIView):
    queryset: Record = Record.objects.all()
    serializer_class: Any = RecordSerializer
    permission_classes: list = [permissions.IsAuthenticated, permissions.IsAdminUser]
    lookup_field: str = "pk"

    def perform_destroy(self, instance) -> Any:
        super().perform_destroy(instance)


record_delete_view: Any = RecordDestroyAPIView.as_view()
