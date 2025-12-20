
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name="کاربر")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True,verbose_name="پروفایل کاربر")
    bio = models.TextField(blank=True,verbose_name="بیوگرافی")

    class Meta:
        verbose_name_plural="پروفایل"

class Category(models.Model):
    title = models.CharField(max_length=100, unique=True,verbose_name="عنوان")

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural="موضوعات"

    

class Book(models.Model):
    title = models.CharField(max_length=200,verbose_name="عنوان")
    author = models.CharField(max_length=200,verbose_name="نویسنده")
    description = models.TextField(verbose_name="توضیحات")
    price = models.PositiveIntegerField(verbose_name="قیمت")
    cover = models.ImageField(upload_to='covers/',verbose_name="جلدکتاب")
    preview_file = models.FileField(upload_to='previews/',verbose_name="مقدمه")  
    full_file = models.FileField(upload_to='books/',verbose_name="فایل اصلی")
    categories = models.ManyToManyField(Category, related_name='books',verbose_name=":زیرشاخه")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="زمان ایجاد")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="زمان بروز رسانی")
    
    is_free = models.BooleanField(default=False,verbose_name="رایگان")

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural="کتاب ها"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders',verbose_name="کاربر")
    is_paid = models.BooleanField(default=False,verbose_name="پرداخت شده")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="زمان ایجاد")

    def total_price(self):
        return sum(item.price for item in self.items.all())
    class Meta:
        verbose_name_plural="سبدخرید"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items',verbose_name="کالا")
    book = models.ForeignKey(Book, on_delete=models.CASCADE,verbose_name="کتاب")
    price = models.PositiveIntegerField(verbose_name="قیمت")
    
    class Meta:
        verbose_name="آیتم"
        verbose_name_plural ="آیتم های سبدخرید"

class Library(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='library',verbose_name="کاربر")
    book = models.ForeignKey(Book, on_delete=models.CASCADE,verbose_name="کتاب")
    added_at = models.DateTimeField(auto_now_add=True,verbose_name="زمان اضافه شدن")

    class Meta:
        verbose_name_plural = 'کتابخانه'
        unique_together = ('user', 'book')

class ReadingProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="کاربر")
    book = models.ForeignKey(Book, on_delete=models.CASCADE,verbose_name="کتاب")
    last_page = models.PositiveIntegerField(default=1,verbose_name="آخرین صفحه خوانده شده")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="زمان بروز رسانی")

    class Meta:
        verbose_name_plural="نشان گذار مطالعه"
        

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist',verbose_name="کاربر")
    book = models.ForeignKey(Book, on_delete=models.CASCADE,verbose_name="کتاب")
    added_at = models.DateTimeField(auto_now_add=True,verbose_name="زمان اضافه شدن")

    class Meta:
        verbose_name_plural ="علاقه مندی ها"
        unique_together = ('user', 'book')

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="کاربر")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews',verbose_name="کتاب")
    rating = models.PositiveIntegerField(default=5,verbose_name="امتیازدهی") 
    comment = models.TextField(blank=True,verbose_name="نظرات")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="زمان ایجاد")

    class Meta:
        verbose_name_plural="بازخوردها"
