from django.contrib import admin
from .models import Category, Bird, ProductImage, Review


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("icon", "name", "order")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("order",)


@admin.register(Bird)
class BirdAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "discount_percent", "final_price_display", "stock", "is_featured", "is_active")
    list_filter = ("category", "care_level", "can_talk", "is_featured", "is_active")
    search_fields = ("name", "species", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("price", "discount_percent", "stock", "is_featured", "is_active")
    inlines = [ProductImageInline]

    @admin.display(description="قیمت نهایی")
    def final_price_display(self, obj):
        return f"{obj.final_price:,} تومان"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("bird", "user", "rating", "is_approved", "created_at")
    list_filter = ("is_approved", "rating")
    list_editable = ("is_approved",)
