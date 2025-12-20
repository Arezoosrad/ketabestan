from django.contrib import admin
from core.models import Book,Profile,ReadingProgress,Review,Order,OrderItem,Wishlist,Library,Category

# Register your models here.

admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Wishlist)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(ReadingProgress)


