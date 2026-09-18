from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from orders.models import Order
from .forms import RegisterForm, LoginForm


def register(request):
    if request.user.is_authenticated:
        return redirect("shop:home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "ثبت‌نام با موفقیت انجام شد. خوش آمدید!")
            return redirect("shop:home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("shop:home")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "با موفقیت وارد شدید.")
            next_url = request.POST.get("next") or request.GET.get("next") or "shop:home"
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.info(request, "از حساب کاربری خارج شدید.")
    return redirect("shop:home")


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "accounts/profile.html", {"orders": orders})
