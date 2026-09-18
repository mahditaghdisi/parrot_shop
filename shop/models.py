from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField("نام دسته", max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True, allow_unicode=True)
    icon = models.CharField("آیکون (ایموجی)", max_length=10, default="🐦")
    image = models.ImageField("تصویر", upload_to="categories/", blank=True, null=True)
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop:category_detail", args=[self.slug])


class Bird(models.Model):
    GENDER_CHOICES = [("M", "نر"), ("F", "ماده"), ("U", "نامشخص")]
    LEVEL_CHOICES = [
        ("easy", "مناسب مبتدی"),
        ("medium", "نیاز به تجربه متوسط"),
        ("pro", "نیاز به نگهدارنده حرفه‌ای"),
    ]

    category = models.ForeignKey(Category, related_name="birds", on_delete=models.CASCADE, verbose_name="دسته‌بندی")
    name = models.CharField("نام", max_length=150)
    slug = models.SlugField(max_length=180, unique=True, blank=True, allow_unicode=True)
    species = models.CharField("گونه", max_length=150, blank=True)
    gender = models.CharField("جنسیت", max_length=1, choices=GENDER_CHOICES, default="U")
    age_months = models.PositiveIntegerField("سن (ماه)", default=0)
    color = models.CharField("رنگ", max_length=80, blank=True)
    care_level = models.CharField("سطح نگهداری", max_length=10, choices=LEVEL_CHOICES, default="easy")
    can_talk = models.BooleanField("سخن‌گو", default=False)
    image = models.ImageField("تصویر اصلی", upload_to="birds/", blank=True, null=True)
    short_description = models.CharField("توضیح کوتاه", max_length=255, blank=True)
    description = models.TextField("توضیحات کامل", blank=True)
    price = models.PositiveIntegerField("قیمت (تومان)")
    discount_percent = models.PositiveIntegerField("درصد تخفیف", default=0)
    stock = models.PositiveIntegerField("موجودی", default=0)
    is_featured = models.BooleanField("محصول ویژه", default=False)
    is_active = models.BooleanField("فعال", default=True)
    created_at = models.DateTimeField("تاریخ ثبت", auto_now_add=True)

    class Meta:
        verbose_name = "پرنده"
        verbose_name_plural = "پرنده‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name, allow_unicode=True) or "bird"
            slug = base
            i = 1
            while Bird.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.slug])

    @property
    def final_price(self):
        if self.discount_percent:
            return int(self.price * (100 - self.discount_percent) / 100)
        return self.price

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def average_rating(self):
        agg = self.reviews.filter(is_approved=True).aggregate(models.Avg("rating"))
        return round(agg["rating__avg"] or 0, 1)

    @property
    def rating_count(self):
        return self.reviews.filter(is_approved=True).count()


class ProductImage(models.Model):
    bird = models.ForeignKey(Bird, related_name="gallery", on_delete=models.CASCADE, verbose_name="پرنده")
    image = models.ImageField("تصویر", upload_to="birds/gallery/")

    class Meta:
        verbose_name = "تصویر گالری"
        verbose_name_plural = "تصاویر گالری"

    def __str__(self):
        return f"تصویر {self.bird.name}"


class Review(models.Model):
    bird = models.ForeignKey(Bird, related_name="reviews", on_delete=models.CASCADE, verbose_name="پرنده")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    rating = models.PositiveSmallIntegerField("امتیاز", choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField("نظر", blank=True)
    is_approved = models.BooleanField("تایید شده", default=True)
    created_at = models.DateTimeField("تاریخ", auto_now_add=True)

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ["-created_at"]
        unique_together = ("bird", "user")

    def __str__(self):
        return f"{self.user} - {self.bird} ({self.rating})"
