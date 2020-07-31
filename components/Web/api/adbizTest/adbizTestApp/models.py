from django.db import models
from django.forms import ModelForm
from django.utils.html import format_html

from django.utils import timezone
# Create your models here.
import django_tables2 as tables
from dynamic_models.models import ModelSchema, FieldSchema

container_object = "container_"
for i in range(1,5):
    container_object = "container_" + str(i)
    container_schema = ModelSchema.objects.create(name = container_object)

    container_object = container_schema.as_model()

Car.objects.create()
assert Car.objects.count() == 1


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

class Person(models.Model):
    class Meta:
        db_table = "Person"

    first_name = models.CharField(max_length=64, unique=True)
    last_name = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)
    dob = models.DateTimeField(default=timezone.now())


class CountryTable(tables.Table):
    class Meta:
        model = Country
        cols = tables.Column()

        print("$$$", cols)
        template_name = "CountryTable.html"
        #fields = ("country_code", "country_name")
