
import django_tables2 as tables
from .models import Person

data = [
{"name": "Bradley"},
{"name": "Stevie"},
]

class PersonTable(tables.Table):
    class Meta:
        model = Person
        template_name = "django_tables2/bootstrap.html"