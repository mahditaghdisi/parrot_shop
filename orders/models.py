from django.conf import settings
from django.db import models
from shop.models import Bird


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار پرداخت"),
        ("paid", "پرداخت شده"),
        ("processing", "در حال آماده‌سازی"),
        ("shipped", "ارسال شده"),
        ("delivered", "تحویل داده شده"),
        ("cancelled", "لغو شده"),
    ]
    PAYMENT_CHOICES = [
        ("cod", "پرداخت در محل"),
        ("online", "پرداخت آنلاین (زرین‌پال)"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    full_name = models.CharField("نام و نام خانوادگی", max_length=150)
    phone = models.CharField("شماره موبایل", max_length=15)
    province = models.CharField("استان", max_length=100)
    city = models.CharField("شهر", max_length=100)
    address = models.TextField("آدرس کامل")
    postal_code = models.CharField("کد پستی", max_length=10, blank=True)
    payment_method = models.CharField("روش پرداخت", max_length=10, choices=PAYMENT_CHOICES, default="cod")
    status = models.CharField("وضعیت", max_length=12, choices=STATUS_CHOICES, default="pending")
    notes = models.TextField("توضیحات سفارش", blank=True)
    created_at = models.DateTimeField("تاریخ ثبت", auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return f"سفارش #{self.id} - {self.full_name}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    bird = models.ForeignKey(Bird, related_name="order_items", on_delete=models.PROTECT)
    price = models.PositiveIntegerField("قیمت واحد (تومان)")
    quantity = models.PositiveIntegerField("تعداد", default=1)

    def __str__(self):
        return f"{self.quantity} x {self.bird.name}"

    def get_cost(self):
        return self.price * self.quantity
