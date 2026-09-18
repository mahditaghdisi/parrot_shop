from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from .models import Category, Bird
from .forms import ReviewForm


def home(request):
    categories = Category.objects.all()
    featured = Bird.objects.filter(is_active=True, is_featured=True)[:8]
    newest = Bird.objects.filter(is_active=True)[:8]
    discounted = Bird.objects.filter(is_active=True, discount_percent__gt=0)[:8]
    return render(request, "shop/home.html", {
        "categories": categories,
        "featured": featured,
        "newest": newest,
        "discounted": discounted,
    })


def product_list(request, category_slug=None):
    birds = Bird.objects.filter(is_active=True)
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        birds = birds.filter(category=category)

    query = request.GET.get("q", "").strip()
    if query:
        birds = birds.filter(Q(name__icontains=query) | Q(species__icontains=query) | Q(description__icontains=query))

    care_level = request.GET.get("level")
    if care_level:
        birds = birds.filter(care_level=care_level)

    can_talk = request.GET.get("can_talk")
    if can_talk:
        birds = birds.filter(can_talk=True)

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price:
        birds = birds.filter(price__gte=min_price)
    if max_price:
        birds = birds.filter(price__lte=max_price)

    sort = request.GET.get("sort", "new")
    sort_map = {
        "new": "-created_at",
        "price_asc": "price",
        "price_desc": "-price",
        "popular": "-is_featured",
    }
    birds = birds.order_by(sort_map.get(sort, "-created_at"))

    paginator = Paginator(birds, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "shop/product_list.html", {
        "page_obj": page_obj,
        "category": category,
        "categories": Category.objects.all(),
        "query": query,
        "sort": sort,
        "care_level": care_level,
    })


def product_detail(request, slug):
    bird = get_object_or_404(Bird, slug=slug, is_active=True)
    related = Bird.objects.filter(category=bird.category, is_active=True).exclude(pk=bird.pk)[:4]
    reviews = bird.reviews.filter(is_approved=True)
    form = ReviewForm()
    user_can_review = request.user.is_authenticated and not bird.reviews.filter(user=request.user).exists()

    if request.method == "POST" and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid() and user_can_review:
            review = form.save(commit=False)
            review.bird = bird
            review.user = request.user
            review.save()
            messages.success(request, "نظر شما با موفقیت ثبت شد.")
            return redirect(bird.get_absolute_url())

    return render(request, "shop/product_detail.html", {
        "bird": bird,
        "related": related,
        "reviews": reviews,
        "form": form,
        "user_can_review": user_can_review,
    })
