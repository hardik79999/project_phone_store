from django import forms
from django.forms import inlineformset_factory
from .models import Product, Specification

# 1. Main Product Form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'price', 'image']
        
        # Bootstrap styling ke liye widgets
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'unique-product-slug'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Product details...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    # Custom Validation: Price 0 se bada hona chahiye
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

# 2. Dynamic Specifications Formset (Add Multiple Specs)
# Yeh 'Product' aur 'Specification' ko jodta hai taaki ek saath save ho sakein
SpecificationFormSet = inlineformset_factory(
    Product, 
    Specification,
    fields=['key_name', 'value'],
    extra=1,  # By default 1 khali box dikhega
    can_delete=True, # User spec delete kar sake
    widgets={
        'key_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Spec Name (e.g. RAM)'}),
        'value': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Value (e.g. 8GB)'}),
    }
)