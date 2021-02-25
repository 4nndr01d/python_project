from django import forms
from .models import Train
from cities.models import City

class TrainForm(forms.ModelForm):
    name = forms.CharField(label='Train',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control',
                                      'placeholder': 'Enter train number'}))

    from_city = forms.ModelChoiceField(label='Starting city',
                                       queryset=City.objects.all(),
                                       widget=forms.Select(
                                           attrs={'class':'form-control'}
                                       ))
    to_city = forms.ModelChoiceField(label='End city',
                                       queryset=City.objects.all(),
                                       widget=forms.Select(
                                           attrs={'class': 'form-control'}
                                       ))

    travel_time = forms.IntegerField(label='Travel time',
                           widget=forms.NumberInput(
                               attrs={'class': 'form-control',
                                      'placeholder': 'Travel time'}))

    class Meta(object):
        model = Train
        fields = ('name', 'from_city', 'to_city', 'travel_time')