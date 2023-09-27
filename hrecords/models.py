from django.db import models
from users.models import CustomUser
from typing import Any
from datetime import date


# Create your models here.
class Record(models.Model):
    patient: Any = models.ForeignKey(
        CustomUser, related_name="patients", on_delete=models.CASCADE
    )
    doctor: Any = models.CharField(max_length=100)
    diagnosis: Any = models.TextField()
    treatment: Any = models.TextField()
    date_of_treatment: Any = models.DateField(auto_now_add=date.today(), blank=True)

    def __str__(self):
        return "({} {}) -> {}".format(
            self.patient.surname, self.patient.other_names, self.date_of_treatment
        )

    class Meta:
        ordering = ["date_of_treatment"]
