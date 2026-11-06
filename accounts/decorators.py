from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect


def seller_required(view_func):
    """Allow only sellers with an active subscription."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in first.")
            return redirect('login')

        if not request.user.is_seller:
            messages.error(request, "This page is for sellers only.")
            return redirect('home')

        seller = getattr(request.user, 'seller_profile', None)
        if not seller:
            messages.error(request, "Seller profile not found. Please contact the administrator.")
            return redirect('home')

        if not seller.is_active_seller:
            if seller.status == 'pending':
                messages.warning(
                    request,
                    "Your account is pending approval. Please pay the subscription fee to start listing products."
                )
            elif seller.status == 'suspended':
                messages.error(request, "Your account has been suspended. Please contact the administrator.")
            else:
                messages.warning(
                    request,
                    "Your subscription has expired. Please renew to continue listing products."
                )
            return redirect('seller_pending')

        return view_func(request, *args, **kwargs)
    return _wrapped