from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, SellerProfile
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Your username',
            'autofocus': True,
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Your password',
        })

class CustomerRegisterForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=False, label="Phone number")

    class Meta:
        model = User
        fields = ('username', 'email', 'phone')


class SellerRegisterForm(UserCreationForm):
    shop_name = forms.CharField(
        max_length=100,
        label="Shop name",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Mama Asha Shop'}),
    )
    phone = forms.CharField(
        max_length=15,
        label="Phone (M-Pesa)",
        widget=forms.TextInput(attrs={'placeholder': '+255 7XX XXX XXX'}),
    )
    whatsapp = forms.CharField(
        max_length=15,
        required=False,
        label="WhatsApp (optional)",
        widget=forms.TextInput(attrs={'placeholder': '+255 7XX XXX XXX'}),
    )
    location = forms.CharField(
        max_length=100,
        required=False,
        label="Location (optional)",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Dar es Salaam'}),
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ondoa help_text zote zenye kelele
        for field in self.fields.values():
            field.help_text = None

        # Weka placeholders kwa fields za msingi
        self.fields['username'].widget.attrs['placeholder'] = 'Choose a username'
        self.fields['email'].widget.attrs['placeholder'] = 'you@example.com'
        self.fields['password1'].widget.attrs['placeholder'] = 'At least 8 characters'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat your password'

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