from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('cash_on_delivery', 'Cash on Delivery'),
    ]
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES)

    class Meta:
        model = Order
        fields = ['address', 'phone_number', 'payment_method']


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=Order.STATUS_CHOICES),
        }


class PaymentForm(forms.Form):
    stripe_token = forms.CharField(widget=forms.HiddenInput)