from django.db import models
from django.forms import ModelForm

from django.utils import timezone
# Create your models here.

class Country(models.Model):
    class Meta:
        db_table = "Country"

    country_code = models.CharField(max_length=3, unique=True, verbose_name="Country Code")
    country_name = models.CharField(max_length=64, unique=True, verbose_name="Country Name")
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now())
    create_by = models.CharField(max_length=64)

    def __str__(self):
        return self.country_name



class State(models.Model):
    class Meta:
        db_table = "State"

    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    state_code = models.CharField(max_length=3, unique=True)
    state_name = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now())
    create_by = models.CharField(max_length=64)

    def __str__(self):
        return self.state_name

