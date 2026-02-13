from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallet'
    )
    balance = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.balance} تومان"
    
    def charge(self, amount):
        self.balance += amount
        self.save()
        Transaction.objects.create(
            user=self.user,
            amount=amount,
            transaction_type='charge',
            description=f'شارژ حساب به مبلغ {amount} تومان'
        )
        return self.balance
    
    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            Transaction.objects.create(
                user=self.user,
                amount=-amount,
                transaction_type='purchase',
                description=f'خرید به مبلغ {amount} تومان'
            )
            return True
        return False

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('charge', 'شارژ'),
        ('purchase', 'خرید'),
        ('refund', 'عودت'),
        ('bonus', 'هدیه'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.get_transaction_type_display()}"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)