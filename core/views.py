
from core.models import Category,OrderItem,Book,Wishlist,Review,Order,ReadingProgress,Library
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from django.contrib import messages 
from core.forms import ReviewForm
from django.conf import settings
from django.db.models import Q,Avg,Sum
from wallet_app.models import Wallet, Transaction
from django.shortcuts import render, redirect,get_object_or_404


# Create your views here.

def home(request):
    books=Book.objects.filter(categories__title="تازه ها").distinct()

    context={
        "books":books
        }
        
    return render(request,"core/index.html",context=context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request,'core/book_detail.html', {
        'book': book,
        'user': request.user  
    })



@login_required
def book_delete(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    messages.success(request,"کتاب با موفقیت حذف شد ✅")
    return redirect("home")




def about_us(request): 
    return render(request, "core/about_us.html")


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save() 
            messages.success(request, f'✅ کتاب "{book.title}" با موفقیت اضافه شد!')
            return redirect('book_detail', book_id=book.id)  
    else:
        form = BookForm()

    return render(request, 'core/add_book.html', {'form': form})


def booksgroup(request):
    Categories=Category.objects.all()
    context={"categories":Categories}
    return render(request, 'core/booksgroup.html', context=context)


def category_books(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    books = Book.objects.filter(categories=category)
    return render(request, 'core/category_books.html', {
        'books': books,
        'category': category
    })

  


def search(request):
    query = request.GET.get('q', '').strip()
    results = []
    message = ''
    results_count = 0
    
    if query:
        try:
            results = Book.objects.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
            
            results_count = results.count()
            
            if results_count == 0:
                message = f'نتیجه‌ای برای "{query}" یافت نشد.'
            else:
                message = f'{results_count} نتیجه برای "{query}"'
                
        except Exception as e:
            message = f'خطا در جستجو: {str(e)}'
            results = []
    
    context = {
        'query': query,
        'results': results,
        'results_count': results_count,
        'message': message,
    }
    
    return render(request,'core/search.html',context)

@login_required
def book_reviews(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all()  

    if request.method == "POST":
        rating = request.POST.get("rating", 5)
        comment = request.POST.get("comment", "")
        Review.objects.create(
            user=request.user,
            book=book,
            rating=rating,
            comment=comment
        )

        return redirect('book_reviews', book_id=book.id)   

    return render(request,'core/book_reviews.html', {
        'book': book,
        'reviews': reviews
    })


@login_required
def cart_detail(request):
    order, created = Order.objects.get_or_create(
        user=request.user,
        is_paid=False,
        defaults={'is_paid': False}
    )
    
    items = order.items.all()
    total_price = order.total_price()
    
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    
    return render(request, 'core/cart_detail.html', {
        'order': order,
        'items': items,  
        'total_price': total_price,
        'wallet_balance': wallet.balance,
        'wallet': wallet
    })


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    order, created = Order.objects.get_or_create(
        user=request.user,
        is_paid=False,
        defaults={'is_paid': False}
    )
    
    order_item = order.items.filter(book=book).first()
    
    if order_item:
        messages.info(request, f'کتاب "{book.title}" قبلاً به سبد خرید اضافه شده است.')
    else:
        OrderItem.objects.create(
            order=order,
            book=book,
            price=book.price
        )
        messages.success(request, f'کتاب "{book.title}" به سبد خرید اضافه شد.')
    
    return redirect('cart_detail')


@login_required
def remove_from_cart(request, item_id):
    order_item = get_object_or_404(
        OrderItem, 
        id=item_id, 
        order__user=request.user, 
        order__is_paid=False
    )
    book_title = order_item.book.title
    order_item.delete()
    messages.success(request, f'کتاب "{book_title}" از سبد خرید حذف شد.')
    return redirect('cart_detail')


@login_required
def clear_cart(request):
    try:
        order = Order.objects.get(user=request.user, is_paid=False)
        order.items.all().delete()
        messages.success(request, 'سبد خرید شما خالی شد.')
    except Order.DoesNotExist:
        pass
    return redirect('cart_detail')





@login_required
def user_library(request):
    library_items = Library.objects.filter(user=request.user).select_related('book').order_by('-added_at')
    
    for item in library_items:
        try:
            progress = ReadingProgress.objects.get(user=request.user, book=item.book)
            item.current_progress = progress  
        except ReadingProgress.DoesNotExist:
            item.current_progress = None
    
    query = request.GET.get('q')
    if query:
        library_items = library_items.filter(
            Q(book__title__icontains=query) | 
            Q(book__author__icontains=query)
        )
    
    return render(request, 'core/user_library.html', {
        'library_items': library_items,
        'total_books': library_items.count()
    })



@login_required
def reading_progress(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        last_page = request.POST.get('last_page')
        
        if not Library.objects.filter(user=request.user, book=book).exists():
            messages.error(request, 'شما به این کتاب دسترسی ندارید.')
            return redirect('user_library')
        
        try:
            last_page = int(last_page)
            if last_page < 1:
                last_page = 1
                
            progress, created = ReadingProgress.objects.update_or_create(
                user=request.user,
                book=book,
                defaults={'last_page': last_page}
            )
            messages.success(request, f'✅ پیشرفت مطالعه ذخیره شد. صفحه {last_page}')
        except (ValueError, TypeError):
            messages.error(request, '❌ شماره صفحه معتبر نیست.')
            
    return redirect('library')    


@login_required
def favorite_books(request):
    favorites = Wishlist.objects.filter(user=request.user).select_related('book').order_by('-added_at')
    
    query = request.GET.get('q')
    if query:
        favorites = favorites.filter(
            Q(book__title__icontains=query) | 
            Q(book__author__icontains=query)
        )
    
    return render(request, 'core/favorite_books.html', {
        'favorites': favorites,
        'total_favorites': favorites.count()
    })


@login_required
def plusfavor(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    favorite, created = Wishlist.objects.get_or_create(
        user=request.user,
        book=book
    )
    
    if created:
        messages.success(request, f'کتاب "{book.title}" به علاقه‌مندی‌ها اضافه شد.')
    else:
        favorite.delete()
        messages.success(request, f'کتاب "{book.title}" از علاقه‌مندی‌ها حذف شد.')
    
    return redirect(request.META.get('HTTP_REFERER', 'book_detail'))




@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    book_id = review.book.id
    review.delete()
    messages.success(request, 'بازخورد شما حذف شد.')
    return redirect('book_detail', book_id=book_id)





@login_required
def payment_verify(request):
    if request.method == 'POST':
        try:
            order = Order.objects.get(user=request.user, is_paid=False)
            
            order.is_paid = True
            order.save()
            
            books_added = []
            for item in order.items.all():
                library_item, created = Library.objects.get_or_create(
                    user=request.user,
                    book=item.book
                )
                books_added.append(item.book.title)
            
            messages.success(
                request, 
                f'✅ پرداخت آنلاین با موفقیت انجام شد! {len(books_added)} کتاب به کتابخانه شما اضافه شد.'
            )
            
            return redirect('user_library')
            
        except Order.DoesNotExist:
            messages.error(request, 'سبد خریدی برای پرداخت وجود ندارد.')
            return redirect('cart_detail')
    
    return redirect('cart_detail')

@login_required
def checkout(request):
    try:
        order = Order.objects.get(user=request.user, is_paid=False)
        items = order.items.all()
        total_price = order.total_price()
    except Order.DoesNotExist:
        messages.error(request, 'سبد خرید شما خالی است.')
        return redirect('cart_detail')
    
    if not items.exists():
        messages.error(request, 'سبد خرید شما خالی است.')
        return redirect('cart_detail')
    
    return render(request,'core/checkout.html', {
        'order': order,
        'items': items,
        'total_price': total_price
    })