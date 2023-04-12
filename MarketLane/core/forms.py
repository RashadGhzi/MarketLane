from .models import CustomerAddress
from django import forms

class CustomerAddressForm(forms.ModelForm):
    class Meta:
        model = CustomerAddress
        fields = ['name','address','city','state','zip_code','phone']