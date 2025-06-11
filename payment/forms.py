from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(max_length=255, required=True)
    shipping_email = forms.CharField(max_length=255, required=True)
    shipping_address1 = forms.CharField(max_length=255, required=True)
    shipping_address2 = forms.CharField(max_length=255, required=False)
    shipping_city = forms.CharField(max_length=255, required=True)
    shipping_zipcode = forms.CharField(max_length=255, required=False)
    shipping_country = forms.CharField(max_length=255, required=True)
    
    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_zipcode', 'shipping_country']
        
        exclude = ['user',]
        
class PaymentForm(forms.Form):
    card_name = forms.CharField(max_length=100, required=True)
    card_number = forms.CharField(max_length=200, required=True)
    card_exp_date = forms.DateField(required=True)
    card_cvv_number = forms.CharField(max_length=100, required=True)
    card_address1 = forms.CharField(max_length=100, required=True)
    card_address2 = forms.CharField(max_length=100, required=False)
    card_city = forms.CharField(max_length=100, required=True)
    card_zipcode = forms.CharField(max_length=100, required=True)
    card_country = forms.CharField(max_length=100, required=True)