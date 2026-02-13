from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q, Sum, Avg
from core.models import Book, Category, Order, OrderItem, Library, Wishlist, Review, ReadingProgress
from wallet_app.models import Wallet, Transaction
from django.conf import settings




@login_required
def wallet_detail(request):
    """نمایش جزئیات کیف پول"""
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    return render(request,'wallet_app/wallet_detail.html', {
        'wallet': wallet,
        'transactions': transactions,
        'balance': wallet.balance
    })


@login_required
def charge_wallet(request):
    """شارژ کیف پول - هم GET و هم POST"""
    
    if request.method == 'GET':
        return render(request, 'wallet_app/charge_wallet.html') 
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        
        try:
            amount = int(amount)
            if amount < 1000:
                messages.error(request, 'حداقل مبلغ شارژ ۱,۰۰۰ تومان است.')
                return redirect('wallet_detail')
            
            wallet, created = Wallet.objects.get_or_create(user=request.user)
            wallet.balance += amount
            wallet.save()
            
            Transaction.objects.create(
                user=request.user,
                amount=amount,
                transaction_type='charge',
                description=f'شارژ کیف پول به مبلغ {amount:,} تومان'
            )
            
            messages.success(request, f'کیف پول شما به مبلغ {amount:,} تومان شارژ شد.')
            
        except (ValueError, TypeError):
            messages.error(request, 'مبلغ وارد شده معتبر نیست.')
            
        return redirect('wallet_detail')



@login_required
@transaction.atomic
def purchase_from_wallet(request):
    """خرید از طریق کیف پول و اضافه شدن به کتابخانه"""
    if request.method == 'POST':
        try:
            order = Order.objects.get(user=request.user, is_paid=False)
        except Order.DoesNotExist:
            messages.error(request, 'سبد خرید شما خالی است.')
            return redirect('cart_detail')
        
        items = order.items.all()
        
        if not items.exists():
            messages.error(request, 'سبد خرید شما خالی است.')
            return redirect('cart_detail')
        
        total_price = order.total_price()
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        
        if wallet.balance >= total_price:
            try:
                success = wallet.withdraw(total_price)
                
                if not success:
                    messages.error(request, 'خطا در برداشت از کیف پول.')
                    return redirect('cart_detail')
                
                order.is_paid = True
                order.save()
                
                books_added = []
                for item in items:
                    library_item, created = Library.objects.get_or_create(
                        user=request.user,
                        book=item.book
                    )
                    books_added.append(item.book.title)
                
                Transaction.objects.create(
                    user=request.user,
                    amount=-total_price,
                    transaction_type='purchase',
                    description=f'خرید {items.count()} کتاب از فروشگاه'
                )
                
                books_list = '، '.join(books_added[:3])
                if len(books_added) > 3:
                    books_list += f' و {len(books_added) - 3} کتاب دیگر'
                
                messages.success(
                    request, 
                    f'✅ خرید با موفقیت انجام شد! {len(books_added)} کتاب به کتابخانه شما اضافه شد. مبلغ پرداخت: {total_price:,} تومان'
                )
                
                return redirect('user_library')
                
            except Exception as e:
                messages.error(request, f'خطا در انجام تراکنش: {str(e)}')
                return redirect('cart_detail')
        else:
            messages.error(
                request, 
                f'❌ موجودی کیف پول کافی نیست! موجودی: {wallet.balance:,.0f} تومان - مبلغ مورد نیاز: {total_price:,.0f} تومان'
            )
            return redirect('cart_detail')
    
    return redirect('cart_detail')
