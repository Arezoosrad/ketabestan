from django import forms
from .models import Book, Category, Review

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'price', 'cover', 'preview_file', 'full_file', 'categories', 'is_free']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان کتاب'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام نویسنده'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'توضیحات کتاب', 'rows': 5}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'قیمت به تومان'}),
            'cover': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'preview_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'full_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'categories': forms.CheckboxSelectMultiple(),
            'is_free': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        labels = {
            'title': 'عنوان',
            'author': 'نویسنده',
            'description': 'توضیحات',
            'price': 'قیمت',
            'cover': 'جلد کتاب',
            'preview_file': 'مقدمه',
            'full_file': 'فایل اصلی',
            'categories': 'زیرشاخه',
            'is_free': 'رایگان',
        }



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.HiddenInput(),  
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'نظر خود را درباره این کتاب بنویسید...',
                'style': 'background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 12px;',
                'required': 'required'
            })
        }
        labels = {
            'rating': 'امتیاز شما',
            'comment': 'نظر شما'
        }


