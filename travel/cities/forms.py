from django import forms
from .models import City

class HtmlForm(forms.Form):
    name = forms.CharField(label='City')

class CityForm(forms.ModelForm):
    name = forms.CharField(label='City',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control',
                                      'placeholder': 'Enter city'}))
    class Meta(object):
        model = City
        fields = ('name', )