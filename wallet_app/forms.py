from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ChargeWalletForm(forms.Form):
    amount = forms.IntegerField(
        min_value=10000,
        max_value=10000000,
        label='مبلغ شارژ (تومان)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'مثال: 50000'
        })
    )
    
    payment_method = forms.ChoiceField(
        choices=[
            ('simulated', 'پرداخت شبیه‌سازی شده'),
            ('zarinpal', 'زرین‌پال'),
        ],
        label='روش پرداخت',
        widget=forms.RadioSelect
    )

class PurchaseForm(forms.Form):
    use_wallet = forms.BooleanField(
        required=False,
        initial=True,
        label='پرداخت از کیف پول'
    )