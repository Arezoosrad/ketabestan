from django.urls import path
from accounts.views import profile_view,register,login_view,logout_view

urlpatterns=[
    path('profile/',profile_view,name="profile"),
    path('register/',register,name="register"),
    path('login/',login_view,name="login"),
    path('logout/',logout_view,name="logout"),

]