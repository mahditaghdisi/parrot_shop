from django import forms

QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]


class CartAddForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=QUANTITY_CHOICES, coerce=int, initial=1, label="تعداد")
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
