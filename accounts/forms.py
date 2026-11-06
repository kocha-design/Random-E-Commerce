from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, SellerProfile


class CustomerRegisterForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=False, label="Phone number")

    class Meta:
        model = User
        fields = ('username', 'email', 'phone')


class SellerRegisterForm(UserCreationForm):
    shop_name = forms.CharField(max_length=100, label="Shop name")
    phone = forms.CharField(max_length=15, label="Phone number (M-Pesa)")
    whatsapp = forms.CharField(max_length=15, required=False, label="WhatsApp (optional)")
    location = forms.CharField(max_length=100, required=False, label="Location")

    class Meta:
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = True
        user.is_customer = False
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
            SellerProfile.objects.create(
                user=user,
                shop_name=self.cleaned_data['shop_name'],
                phone=self.cleaned_data['phone'],
                whatsapp=self.cleaned_data.get('whatsapp', ''),
                location=self.cleaned_data.get('location', ''),
                status='pending',
            )
        return user