from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomerRegisterForm, SellerRegisterForm


def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! You have registered as a customer.")
            return redirect('home')
    else:
        form = CustomerRegisterForm()
    return render(request, 'accounts/register_customer.html', {'form': form})


def register_seller(request):
    if request.method == 'POST':
        form = SellerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                "Welcome! Your seller account has been created. Please pay the subscription fee to start listing products."
            )
            return redirect('home')
    else:
        form = SellerRegisterForm()
    return render(request, 'accounts/register_seller.html', {'form': form})


@login_required
def profile_redirect(request):
    """Redirect user to the right place based on their role."""
    user = request.user

    if user.is_staff:
        return redirect('/admin/')

    if user.is_seller:
        seller = getattr(user, 'seller_profile', None)
        if seller and seller.is_active_seller:
            return redirect('seller_dashboard')
        else:
            return redirect('seller_pending')

    return redirect('product_list')