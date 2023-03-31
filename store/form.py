from django import forms
from .models import Product,Order,OrderItem


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields=('category','title','description','price','image','thumbnail')
        widgets ={
            'category':forms.Select(attrs={
            'class': 'w-full p-4 border border-gray-300'
            }),
            'title':forms.TextInput(attrs={
            'class': 'w-full p-4 border border-gray-300'
            }),
            'description':forms.Textarea(attrs={
            'class': 'w-full p-4 border border-gray-300'
            }),
            'price':forms.TextInput(attrs={
            'class': 'w-full p-4 border border-gray-300'
            }),
            'image':forms.FileInput(attrs={
            'class': 'w-full p-4 border border-gray-300'
            }),
            'thumbnail':forms.FileInput(attrs={
            'class': 'w-full p-4 border border-gray-300'
            }),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model= Order
        fields=('first_name','last_name','address','phone_contact','email','city','zip_code',)