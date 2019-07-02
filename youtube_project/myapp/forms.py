from django import forms
from django.forms import Form


class SearchVideo(Form):
    search = forms.CharField(min_length=4, widget=forms.TextInput(attrs={'class': 'form-control'}))

