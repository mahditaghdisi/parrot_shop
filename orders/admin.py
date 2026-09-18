from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["bird"]
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone", "city", "payment_method", "status", "total_display", "created_at")
    list_filter = ("status", "payment_method", "created_at")
    list_editable = ("status",)
    search_fields = ("full_name", "phone", "id")
    inlines = [OrderItemInline]

    @admin.display(description="مبلغ کل")
    def total_display(self, obj):
        return f"{obj.get_total_cost():,} تومان"
