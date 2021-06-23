from django import forms
from core.articles.models import Article


class ArticleForm(forms.ModelForm):
    images = forms.FileField(
        required=True, widget=forms.FileInput(attrs={
            'class': 'form-control',
            'multiple': True,
        }))

    class Meta:
        model = Article
        fields = ('title', 'description', 'price', 'stock', 'status')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type the description', 'rows': 5, 'style': 'resize: none'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Type the price'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Type the amount'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
