from rest_framework import serializers, reverse
from .models import Record
from users.serializers import RegistrationSerializer
from typing import Any


class RecordSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="record-detail", lookup_field="pk"
    )
    update_url: Any = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model: Record = Record
        fields: tuple = (
            "pk",
            "url",
            "doctor",
            "diagnosis",
            "treatment",
            "date_of_treatment",
            "update_url",
        )

    def to_representation(self, instance):
        self.fields["patient"] = RegistrationSerializer(read_only=True)
        return super(RecordSerializer, self).to_representation(instance)

    def get_update_url(self, obj):
        request = self.context.get("request")
        if request:
            return reverse.reverse(
                "record-update", kwargs={"pk": obj.pk}, request=request
            )


class CreateRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model: Record = Record
        fields: tuple = (
            "doctor",
            "diagnosis",
            "treatment",
            "date_of_treatment",
            "patient",
        )

    def to_representation(self, instance):
        self.fields["patient"] = RegistrationSerializer(read_only=True)
        return super(CreateRecordSerializer, self).to_representation(instance)