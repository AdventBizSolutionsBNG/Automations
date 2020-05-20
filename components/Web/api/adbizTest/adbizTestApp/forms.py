from .models import Country
from django import forms


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        #fields = "__all__"
        fields=['country_code', 'country_name', 'is_active']

