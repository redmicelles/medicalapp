from rest_framework import serializers, reverse
from .models import Record
from typing import Any
from users.serializers import serializers as userializer



class RecordSerializer(serializers.ModelSerializer):
    patient = userializer

    class Meta:
        model: Record = Record
        fields: tuple = ("id", "doctor", "diagnosis", "treatment")
        read_only_fields: tuple = ("other_names", "surname", "date_of_birth")

    # def get_patient(self, obj):
    #     return [obj.user.pk, obj.user.surname, obj.user.other_names, obj.user.date_of_birth]
    
    
    # edit_url: Any = serializers.SerializerMethodField(read_only=True)
    # url: Any = serializers.HyperlinkedIdentityField(view_name="record-detail", lookup_field="pk")
    # class Meta:
    #     model: Record = Record
    #     fields: tuple = ("doctor", "diagnosis", "treatment")
    
    # def get_edit_url(self, obj):
    #     request = self.context.get("request")
    #     if request:
    #         return reverse.reverse(
    #             "record-edit",
    #             kwargs={"pk": obj.pk},
    #             request=request
    #         )