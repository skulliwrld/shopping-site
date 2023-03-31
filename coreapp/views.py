from django.shortcuts import render
from store.models import Product

# Create your views here.
def index(request):
    products = Product.objects.filter(status=Product.ACTIVE)[0:6]
    return render(request,'coreapp/frontpage.html',{"products":products})

def about(request):
    return render(request,'coreapp/about.html')