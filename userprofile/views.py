from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import Userprofile
from django.contrib.auth import login
from django.contrib.auth.forms  import UserCreationForm
from store.form import ProductForm
from store.models import Product,Order,OrderItem
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required
def vendor_detail(request,pk):
    user = User.objects.get(pk=pk)
    products= user.products.filter(status=Product.ACTIVE)

    return render(request,'userprofile/vendor_detail.html',{
        'user':user,
        'products':products

    })

def myaccount(request):
    return render(request,"userprofile/myaccount.html")


@login_required
def add_product(request):
    if request.method == 'POST':
       form=ProductForm(request.POST,request.FILES)
       if form.is_valid():
           title=request.POST.get('title')
           slug= slugify(title) 

           product =form.save(commit=False)
           product.user = request.user
           product.slug  = slug
           product.save()
           messages.success(request,'you have successfully added your Product')
           return redirect('mystore')
    else:
        form =ProductForm()
    return render(request,'userprofile/product_form.html',{'form':form,'title':"Add product"})

@login_required
def edit_product(request,product_id):
    product = Product.objects.filter(user=request.user).get(pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,'Product updated successfully')
            return redirect('mystore')
    else:
        form = ProductForm(instance=product) 
    return render(request,"userprofile/product_form.html",{'form':form,'title':'Edit Product','product':product}) 


def delete_product(request,product_id):
    product = Product.objects.filter(user=request.user).get(pk=product_id)
    product.status = Product.DELECTED
    product.save()
    messages.success(request,'product delected successfully')
    return redirect('mystore')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user=form.save()

            login(request,user)

            userprofile =Userprofile.objects.create(user=user)

            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request,'userprofile/signup.html',{'form':form})

@login_required
def my_store(request):
    order_items =OrderItem.objects.filter(product__user=request.user)
    products = request.user.products.exclude(status=Product.DELECTED)

    return render(request,'userprofile/my_store.html',{
        'products':products,
        'order_items':order_items,
        })

@login_required
def my_store_order_detail(request,pk):
    order = get_object_or_404(Order,pk=pk)

    return render(request,'store/order_detail.html',{
        'order':order
    })