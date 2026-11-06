from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    is_seller = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.username


class SellerProfile(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    shop_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    whatsapp = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    subscription_end = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_subscription_valid(self):
        if not self.subscription_end:
            return False
        return self.subscription_end >= timezone.now().date()

    @property
    def is_active_seller(self):
        return self.status == 'active' and self.is_subscription_valid()

    def __str__(self):
        return self.shop_name


class Payment(models.Model):
    """Subscription payment record — admin confirms manually after receiving funds."""
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    months = models.PositiveIntegerField(default=1)
    reference = models.CharField(max_length=50, blank=True)  # e.g. M-Pesa reference
    confirmed = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def confirm(self):
        """Admin calls this after seeing the money has arrived."""
        self.confirmed = True
        self.confirmed_at = timezone.now()
        self.save()

        seller = self.seller
        today = timezone.now().date()
        if seller.subscription_end and seller.subscription_end >= today:
            start = seller.subscription_end
        else:
            start = today
        seller.subscription_end = start + timedelta(days=30 * self.months)
        seller.status = 'active'
        seller.save()

    def __str__(self):
        return f"{self.seller.shop_name} — TSh {self.amount} ({self.months} mo)"