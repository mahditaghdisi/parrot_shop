from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages

from shop.models import Bird
from .cart import Cart
from .forms import CartAddForm


@require_POST
def cart_add(request, bird_id):
    cart = Cart(request)
    bird = get_object_or_404(Bird, id=bird_id, is_active=True)
    form = CartAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        if bird.stock < 1:
            messages.error(request, "متاسفانه این پرنده در حال حاضر موجود نیست.")
        else:
            cart.add(bird=bird, quantity=cd["quantity"], override_quantity=cd["override"])
            messages.success(request, f'«{bird.name}» به سبد خرید اضافه شد.')
    return redirect(request.POST.get("next") or "cart:cart_detail")


@require_POST
def cart_remove(request, bird_id):
    cart = Cart(request)
    bird = get_object_or_404(Bird, id=bird_id)
    cart.remove(bird)
    messages.info(request, f'«{bird.name}» از سبد خرید حذف شد.')
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/detail.html", {"cart": cart})
