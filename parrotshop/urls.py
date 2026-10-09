from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
    path("account/", include("accounts.urls")),
    path("", include("shop.urls")),
    # عکس‌های آپلودی (media) هم روی لوکال و هم روی Render سرو می‌شن
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]

admin.site.site_header = "پنل مدیریت پرندگان‌شاپ"
admin.site.site_title = "پرندگان‌شاپ"
admin.site.index_title = "مدیریت فروشگاه"