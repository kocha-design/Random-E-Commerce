from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import seller_required
from .models import Product
from .forms import ProductForm
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category
# products/views.py
from .models import Product, Category


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
    return render(request, 'products/seller_dashboard.html', {
        'seller': seller,
        'products': products,
    })


@seller_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller_profile
            product.save()
            messages.success(request, "Bidhaa imeongezwa kikamilifu.")
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {
        'form': form,
        'title': "Ongeza Bidhaa Mpya",
    })


@seller_required
def product_edit(request, pk):
    seller = request.user.seller_profile
    product = get_object_or_404(Product, pk=pk, seller=seller)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Bidhaa imehaririwa.")
            return redirect('seller_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {
        'form': form,
        'title': "Hariri Bidhaa",
    })


@seller_required
def product_delete(request, pk):
    seller = request.user.seller_profile
    product = get_object_or_404(Product, pk=pk, seller=seller)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Bidhaa imefutwa.")
        return redirect('seller_dashboard')
    return render(request, 'products/product_confirm_delete.html', {'product': product})


# ==================== CUSTOMER / PUBLIC ====================

def product_list(request):
    products = Product.objects.filter(
        is_available=True,
        seller__status='active',
    ).select_related('seller', 'category')
    return render(request, 'products/product_list.html', {'products': products})


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

    categories = Category.objects.all()

    return render(request, 'products/product_list.html', {
        'page_obj': page_obj,
        'products': page_obj,
        'categories': categories,
        'q': q,
        'selected_category': cat_slug,
        'min_price': min_price,
        'max_price': max_price,
    })