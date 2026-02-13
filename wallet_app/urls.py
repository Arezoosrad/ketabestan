from django.urls import path
from . import views

urlpatterns = [
    path('charge-wallet/', views.charge_wallet, name='charge_wallet'),
    path('wallet_detail/',views.wallet_detail,name='wallet_detail'),
    path('purchase_from_wallet',views.purchase_from_wallet,name='purchase_from_wallet')
    
    
]