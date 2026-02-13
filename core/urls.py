
from django.urls import path
from core.views import home,book_detail,category_books,search,booksgroup,about_us,add_book,book_delete,favorite_books,plusfavor,book_reviews,add_to_cart,cart_detail,remove_from_cart,payment_verify,user_library,reading_progress,book_reviews,delete_review,checkout

urlpatterns = [
    path('',home,name='home'),
    path("book/<int:book_id>/",book_detail,name="book_detail"),
    path('booksgroup/',booksgroup,name='booksgroup'),
    path('categories/<int:category_id>/', category_books, name='category_books'),
    path('search/',search, name='search'),
    path('about_us/',about_us,name="darbarema"),
    path('add/', add_book, name='add_book'),
    path('book_delete/<int:book_id>/',book_delete,name="book_delete"),
    path('favorite/add/<int:book_id>/',plusfavor, name='plusfavor'),
    path('favorites/',favorite_books, name='favorite_books'),
    path('cart/',cart_detail, name='cart_detail'),
    path('cart/add/<int:book_id>/',add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/',remove_from_cart, name='remove_from_cart'),
    path('payment/verify/',payment_verify, name='payment_verify'),
    path('library',user_library,name='library'),
    path('reading-progress/<int:book_id>/',reading_progress, name='reading_progress'),
    path('review/<int:book_id>/',book_reviews, name='book_reviews'),
     path('review/<int:book_id>/delete/',delete_review, name='delete_review'),
     path('checkout/', checkout, name='checkout'),
]





