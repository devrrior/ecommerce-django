from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'description', 'price', 'stock', 'status')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type the description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Type the price'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Type the amount'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
