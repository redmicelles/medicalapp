from django.urls import path
from .views import (
    record_list_view,
    record_detail_view,
    record_update_view,
    record_delete_view,
    record_create_view
)

urlpatterns = [
    path("", record_list_view, name="my-records"),
    path("create/", record_create_view, name="record-create"),
    path("<int:pk>/", record_detail_view, name="record-detail"),
    path("<int:pk>/update/", record_update_view, name="record-update"),
    path("<int:pk>/delete/", record_delete_view, name="record-delete"),
]
