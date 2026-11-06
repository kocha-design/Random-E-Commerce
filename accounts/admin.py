from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.urls import path
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from datetime import date, timedelta

from .models import User, SellerProfile, Payment


# ==================== USER ====================

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_seller', 'is_customer', 'is_staff')
    list_filter = ('is_seller', 'is_customer', 'is_staff')
    search_fields = ('username', 'email', 'phone')
    fieldsets = UserAdmin.fieldsets + (
        ('Roles', {'fields': ('is_seller', 'is_customer', 'phone', 'language')}),
    )


# ==================== SELLER ====================

@admin.register(SellerProfile)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'user', 'status', 'subscription_end', 'is_active_seller', 'product_count')
    list_filter = ('status', 'created_at')
    search_fields = ('shop_name', 'user__username', 'phone')
    readonly_fields = ('created_at',)
    actions = ['suspend_sellers', 'activate_sellers', 'extend_30_days']

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "Bidhaa"

    @admin.action(description="Simamisha wauzaji waliochaguliwa")
    def suspend_sellers(self, request, queryset):
        updated = queryset.update(status='suspended')
        self.message_user(request, f"Wauzaji {updated} wamesimamishwa.", messages.WARNING)

    @admin.action(description="Ruhusu wauzaji waliochaguliwa")
    def activate_sellers(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f"Wauzaji {updated} wameruhusiwa.", messages.SUCCESS)

    @admin.action(description="Ongeza siku 30 za subscription")
    def extend_30_days(self, request, queryset):
        for seller in queryset:
            base = (seller.subscription_end
                    if seller.subscription_end and seller.subscription_end >= timezone.now().date()
                    else timezone.now().date())
            seller.subscription_end = base + timedelta(days=30)
            seller.status = 'active'
            seller.save()
        self.message_user(request, f"Wauzaji {queryset.count()} wameongezewa siku 30.", messages.SUCCESS)


# ==================== PAYMENT ====================

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('seller', 'amount', 'months', 'reference', 'confirmed', 'created_at')
    list_filter = ('confirmed', 'created_at')
    search_fields = ('seller__shop_name', 'reference')
    readonly_fields = ('confirmed_at',)
    actions = ['confirm_payments']

    @admin.action(description="Thibitisha malipo (extend subscription)")
    def confirm_payments(self, request, queryset):
        count = 0
        for payment in queryset.filter(confirmed=False):
            payment.confirm()
            count += 1
        self.message_user(
            request,
            f"Malipo {count} yamethibitishwa na subscription imeongezwa.",
            messages.SUCCESS,
        )


# ==================== SUBSCRIPTION ALERTS ====================

@staff_member_required
def subscription_alerts(request):
    today = date.today()
    soon = today + timedelta(days=7)

    expiring_soon = SellerProfile.objects.filter(
        status='active',
        subscription_end__gte=today,
        subscription_end__lte=soon,
    ).order_by('subscription_end')

    expired = SellerProfile.objects.filter(
        status='active',
        subscription_end__lt=today,
    ).order_by('subscription_end')

    pending_payments = Payment.objects.filter(confirmed=False).order_by('-created_at')

    return render(request, 'admin/subscription_alerts.html', {
        'expiring_soon': expiring_soon,
        'expired': expired,
        'pending_payments': pending_payments,
        'title': 'Subscription Alerts',
    })


# ==================== ADMIN URLS ====================

_original_get_urls = admin.site.get_urls

def get_urls():
    urls = _original_get_urls()
    custom_urls = [
        path('subscription-alerts/',
             admin.site.admin_view(subscription_alerts),
             name='subscription_alerts'),
    ]
    return custom_urls + urls

admin.site.get_urls = get_urls
admin.site.site_header = "Soko Letu Admin"
admin.site.site_title = "Soko Letu"
admin.site.index_title = "Usimamizi wa Soko"