import json
import stripe

from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings


from .models import Product,Order,OrderItem
from.models import category
from django.db.models import Q
from .cart import Cart

from.form import OrderForm
# Create your views here.


def category_view(request, slug):
    categoryy = get_object_or_404(category,slug=slug)
    products= categoryy.products.filter(status=Product.ACTIVE)
    return render(request,'store/category_view.html',{
        'categoryy':categoryy,
        'products':products
        })
# CART RENDERATION
def cart_view(request):
    cart = Cart(request)
    return render(request,'store/cart.html',{'cart':cart})

def add_to_cart(request,product_id):
    cart = Cart(request)
    cart.add(product_id)

    return redirect('cart')

def remove_form_cart(request,product_id):
    cart =Cart(request)
    cart.remove(product_id)

    return redirect('cart')

def change_quantity(request,product_id):
    action = request.GET.get('action', '')

    if action:
        quantity = 1

        if action == 'decrease':
            quantity =-1

        cart =Cart(request)
        cart.add(product_id,quantity,True)
    return redirect('cart')

@login_required
def checkout(request):
    cart = Cart(request)
    if cart.get_total_cost() == 0:
        return redirect('cart')
    
    if request.method == 'POST':
        data = json.loads(request.body)
        first_name=data['first_name']
        last_name=data['last_name']
        address=data['address']
        phone_contact=data['phone_contact']
        email=data['email']
        city=data['city']
        zip_code=data['zip_code']

        if first_name and last_name and address and phone_contact and email and city and zip_code:
            form = OrderForm(request.POST)
            
            total_price = 0
            items =[]

            for item in cart:
                product = item['product']
                total_price += product.price * int(item['quantity'])

                # Stripe Payment Gateway
                items.append({
                    'price_data': {
                    'currency': 'usd',
                    'product_data':{
                    'name': product.title,
                    },
                    'unit_amount':product.price
                    },
                    'quantity': item['quantity']
                })
            
            stripe.api_key = settings.STRIPE_SECRET_KEY
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=items,
                mode='payment',
                success_url='http://127.0.0.1:8000/cart/success',
                cancel_url= 'http://127.0.0.1:8000/cart/',

            )
            payment_intent = session.payment_intent


            order = Order.objects.create(
                first_name= first_name,
                last_name=last_name,
                address= address,
                phone_contact=phone_contact ,
                email= email,
                city = city,
                zip_code = zip_code,
                created_by = request.user,
                payment_intent = payment_intent,
                is_paid= True,
                paid_amount = total_price
            )

            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity

                item = OrderItem.objects.create(order=order,product=product,price=price,quantity=quantity)

            cart.clear()
            
            return JsonResponse({'session':session,'order':payment_intent})
    else:
        form = OrderForm()


    return render(request,'store/checkout.html',{
        'cart':cart,
        'form':form,
        'pub_key':settings.STRIPE_PUB_KEY,
    })


def success(request):
    return render(request,'store/success.html')

def search(request):
    query =request.GET.get('query', '')
    products =  Product.objects.filter(status=Product.ACTIVE).filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request,'store/search.html',{
        'query': query,
        'products':products
    })
def product_view(request,category_slug,slug):
    product = get_object_or_404(Product,slug=slug,status=Product.ACTIVE)
    return render(request,'store/product_views.html',{'product':product})
