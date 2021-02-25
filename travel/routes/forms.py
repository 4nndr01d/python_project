from django import forms
from .models import Train
from cities.models import City

class RouteForm(forms.Form):
    from_city = forms.ModelChoiceField(label='Starting city',
                                       queryset=City.objects.all(),
                                       widget=forms.Select(
                                           attrs={'class':'form-control js-example-basic-single'}
                                       ))
    to_city = forms.ModelChoiceField(label='End city',
                                       queryset=City.objects.all(),
                                       widget=forms.Select(
                                           attrs={'class': 'form-control js-example-basic-single'}
                                       ))

    across_cities = forms.ModelMultipleChoiceField(label='Across cities',
                                                   queryset=City.objects.all(),
                                                   required=False,
                                                   widget=forms.SelectMultiple(attrs={'class': 'form-control js-example-basic-multiple'}))

    travel_time = forms.IntegerField(label='Travel time',
                           widget=forms.NumberInput(
                               attrs={'class': 'form-control',
                                      'placeholder': 'Travel time'}))