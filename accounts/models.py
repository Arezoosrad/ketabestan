from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.


class GenderOption(models.TextChoices):
    male=("m","مرد")
    female=("f","زن")
    none=("n","ترجیح می دهم مشخص نکنم")


class User(AbstractUser):
    profile_picture= models.ImageField("عکس پروفایل",upload_to="profile_pictures",default="profile_pictures/default.jpg")
    bio = models.TextField(blank=True,verbose_name="بیوگرافی")
    birthdate=models.DateField("تاریخ تولد",null=True,blank=True)
    gender=models.CharField(max_length=15,choices=GenderOption.choices)
    class Meta:
        verbose_name="کاربر"
        verbose_name_plural="کاربر"

    def __str__(self):
        return f"{self.username}"