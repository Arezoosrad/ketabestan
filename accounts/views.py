from django.shortcuts import render,redirect
from accounts.models import User
from accounts.forms import RegisterForm
from django.contrib import messages
from accounts.forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from django.urls import reverse

def profile_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'شما باید اول لاگین کنید تا صفحه پروفایل را ببینید')
        home_url = reverse('home')
        return redirect(f'{home_url}?next={request.path}')
    
    return render(request, "accounts/profile.html")

def register(request):

    form=RegisterForm()
    if request.method=='POST':
        form=RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            new_user=form.save(commit=False)
            new_user.set_password(new_user.password)
            new_user.save()
            messages.success(request,"ثبت نام شما با موفقیت انجام شد")
            return redirect('login')
    return render(request,'accounts/register.html',{'form':form})



def login_view(request):
    form=LoginForm()
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            login(request,user)
            messages.success(request,"خوش آمدید ")
            return redirect("profile")
    return render(request,"accounts/login.html",{'form':form})


def logout_view(request):
    logout(request)
    messages.success(request,"شما با موفقیت خارج شدید")
    return redirect("login")