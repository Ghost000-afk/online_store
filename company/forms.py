from django import forms
from .models import Company
from products.models import Product


class CompanyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'logo']



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price', 'description', 'category', 'image', 'discount']    
     