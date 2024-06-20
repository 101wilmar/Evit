from django.db import models

from app.models import BaseModel


class Location(BaseModel):
    name = models.CharField(max_length=120)
    duration = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Постоянное место жительства'
        verbose_name_plural = 'Постоянное место жительства'
