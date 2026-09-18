from django.contrib import messages
from django.shortcuts import render, redirect

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem


def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "سبد خرید شما خالی است.")
        return redirect("shop:home")

    initial = {}
    if request.user.is_authenticated:
        initial["full_name"] = request.user.get_full_name() or request.user.username

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    bird=item["bird"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
                bird = item["bird"]
                bird.stock = max(0, bird.stock - item["quantity"])
                bird.save(update_fields=["stock"])
            cart.clear()
            return redirect("orders:order_success", order_id=order.id)
    else:
        form = OrderCreateForm(initial=initial)

    return render(request, "orders/create.html", {"cart": cart, "form": form})


def order_success(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    return render(request, "orders/success.html", {"order": order})
