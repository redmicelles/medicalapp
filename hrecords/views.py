from .models import Record
from .serializers import RecordSerializer
from rest_framework import generics
from rest_framework import permissions
from typing import Any
from common.pydantic_models import URLParams
from rest_framework import exceptions


class RecordListCreateAPIView(generics.ListCreateAPIView):
    queryset: Record = Record.objects.all()
    serializer_class: Any = RecordSerializer
    permission_classes: Any = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return Record.objects.filter(patient=self.request.user).all()
        try:
            Record.objects.filter(patient=self.request.user).all()
        except Record.DoesNotExist:
            raise exceptions.NotFound

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.validated_data
            serializer.save()
        raise exceptions.PermissionDenied


record_list_create_view: Any = RecordListCreateAPIView.as_view()


class RecordDetailAPIView(generics.RetrieveAPIView):
    queryset: Record = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # validate url param
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
        serializer.validated_data
        serializer.save()


record_update_view = RecordUpdateAPIView.as_view()


class RecordDestroyAPIView(generics.DestroyAPIView):
    queryset: Record = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    lookup_field = "pk"

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


record_delete_view = RecordDestroyAPIView.as_view()
