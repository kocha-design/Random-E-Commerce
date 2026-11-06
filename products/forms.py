from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'description', 'price', 'image', 'is_available')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }
        help_texts = {
            'price': 'Price in TSh (e.g., 15000 for TSh 15,000).',
            'image': 'One good image. Recommended size: 800x800.',
            'is_available': 'Uncheck to hide this product from customers temporarily.',
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Price must be greater than 0.")
        return price