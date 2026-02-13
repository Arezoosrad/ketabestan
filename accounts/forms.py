from django import forms
from accounts.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError




class RegisterForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        validators=[FileExtensionValidator(['jpg', 'png'], 'فرمت فایل معتبر نیست')],
        label='عکس پروفایل',
        required=False
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='تکرار گذرواژه'
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'confirm_password',
            'first_name',
            'last_name',
            'birthdate',
            'gender',
            'bio',
            'profile_picture',
        ]
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birthdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
        labels = {
            'username': 'نام کاربری',
            'password': 'گذرواژه',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'birthdate': 'تاریخ تولد',
            'gender': 'جنسیت',
            'bio': 'بیوگرافی',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            if hasattr(field, 'widget'):
                field.widget.attrs['style'] = 'text-align: right; direction: rtl;'

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError('گذرواژه و تکرار آن مطابقت ندارند')
        
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
        
        return user



    def clean_username(self):
        username=self.cleaned_data.get("username")
        user=User.objects.filter(username=username).exists()    
        if user:
            raise forms.ValidationError("کاربری با این نام کاربری قبلا ثبت نام کرده است")
        return username
        

    def clean(self):
        data =self.cleaned_data
        password=data.get('password')
        confirm_password=data.pop('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("گذرواژه با تکرار آن مطابقت ندارد!")
        return data


class LoginForm(forms.Form):
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}),label="نام کابری :")
    password=forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'class':'form-control'}),label="گذرواژه : ")


