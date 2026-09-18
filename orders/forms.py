from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "phone", "province", "city", "address", "postal_code", "payment_method", "notes"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "نام و نام خانوادگی"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "09xxxxxxxxx"}),
            "province": forms.TextInput(attrs={"class": "form-control", "placeholder": "استان"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "شهر"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "آدرس کامل پستی"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "کد پستی"}),
            "payment_method": forms.RadioSelect(),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "توضیحات تکمیلی (اختیاری)"}),
        }
