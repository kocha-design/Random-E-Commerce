from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST   # ← MUHIMU
from django.db.models import Q
from django.core.paginator import Paginator

from accounts.decorators import seller_required
from .models import Product, Category
from .forms import ProductForm
from .cart import Cart
from django.utils import timezone
from django.db.models import Sum

# ==================== HOME ====================

def home(request):
    latest_products = Product.objects.filter(
        is_available=True,
        seller__status='active',
    ).select_related('seller', 'category').order_by('-created_at')[:8]
    categories = Category.objects.all()[:8]
    return render(request, 'home.html', {
        'latest_products': latest_products,
        'categories': categories,
    })


# ==================== SELLER ====================

@seller_required
def seller_dashboard(request):
    seller = request.user.seller_profile
    products = seller.products.all().order_by('-created_at')

    # Takwimu
    available_count = products.filter(is_available=True).count()
    total_value = sum(p.price for p in products)

    # Siku zilizobaki
    days_left = 0
    if seller.subscription_end:
        days_left = (seller.subscription_end - timezone.now().date()).days
        if days_left < 0:
            days_left = 0

    return render(request, 'products/seller_dashboard.html', {
        'seller': seller,
        'products': products,
        'available_count': available_count,
        'total_value': total_value,
        'days_left': days_left,
    })

@seller_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller_profile
            product.save()
            messages.success(request, "Product added successfully.")
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {
        'form': form,
        'title': "Add New Product",
    })


@seller_required
def product_edit(request, pk):
    seller = request.user.seller_profile
    product = get_object_or_404(Product, pk=pk, seller=seller)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated.")
            return redirect('seller_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {
        'form': form,
        'title': "Edit Product",
    })


@seller_required
def product_delete(request, pk):
    seller = request.user.seller_profile
    product = get_object_or_404(Product, pk=pk, seller=seller)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted.")
        return redirect('seller_dashboard')
    return render(request, 'products/product_confirm_delete.html', {'product': product})


# ==================== PUBLIC ====================

def product_list(request):
    products = Product.objects.filter(
        is_available=True,
        seller__status='active',
    ).select_related('seller', 'category')

    q = request.GET.get('q', '').strip()
    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )

    cat_slug = request.GET.get('category', '').strip()
    if cat_slug:
        products = products.filter(category__slug=cat_slug)

    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {
        'page_obj': page_obj,
        'products': page_obj,
        'categories': Category.objects.all(),
        'q': q,
        'selected_category': cat_slug,
        'min_price': min_price,
        'max_price': max_price,
    })


def product_detail(request, pk):
    product = get_object_or_404(
        Product.objects.select_related('seller', 'category'),
        pk=pk,
        is_available=True,
        seller__status='active',
    )
    return render(request, 'products/product_detail.html', {'product': product})


def seller_pending(request):
    return render(request, 'products/seller_pending.html')


# ==================== CART ====================

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    override = request.POST.get('override') == 'True'
    cart.add(product=product, quantity=quantity, override_quantity=override)
    messages.success(request, f"{product.name} added to cart.")
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f"{product.name} removed from cart.")
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    
    # Tengeneza ujumbe wa WhatsApp
    message = "Hello, I'd like to order:\n\n"
    for item in cart:
        message += f"- {item['product'].name} x {item['quantity']} = {item['total_price']} TSh\n"
    message += f"\nTotal: {cart.get_total_price()} TSh"
    
    return render(request, 'cart/detail.html', {
        'cart': cart,
        'whatsapp_message': message,
    })