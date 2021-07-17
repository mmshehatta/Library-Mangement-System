

from django import forms
from django.forms import fields, widgets
from django.forms.models import ModelForm
from . models import Book , Genre

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields=['name']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'})
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields='__all__'
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.Select(attrs={'class':'form-control'}),
            'summary':forms.TextInput(attrs={'class':'form-control'}),
            'isbn':forms.TextInput(attrs={'class':'form-control'}),
            'genre':forms.SelectMultiple(attrs={'class':'form-control'}),
            'language':forms.Select(attrs={'class':'form-control'}),
            'book_img':forms.FileInput(attrs={'class':'form-control'}),
            'author_img':forms.FileInput(attrs={'class':'form-control'}),
            'pages':forms.NumberInput(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'rental_price_day':forms.NumberInput(attrs={'class':'form-control','id':'rentalprice'}),
            'rental_period':forms.NumberInput(attrs={'class':'form-control' , 'id':'rentalperiod'}),
            'total_rental':forms.NumberInput(attrs={'class':'form-control' , 'id':'totlalrental'}),
            'active':forms.CheckboxInput(),
            'status':forms.Select(attrs={'class':'form-control'}),
        }
