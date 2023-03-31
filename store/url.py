from django.urls import path
from .import views

urlpatterns = [
    path('search/',views.search,name="search"),
    path('add_to_cart/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path("cart/",views.cart_view,name='cart'),
    path('cart/checkout/',views.checkout,name='checkout'),
    path('cart/success/',views.success,name="success"),
    path('remove_form_cart/<str:product_id>/',views.remove_form_cart,name="remove_from_cart"),
    path('change_quantity/<int:product_id>/',views.change_quantity,name='change_quantity'),
    path('<slug:slug>/',views.category_view, name='category_view'),
    path('<slug:category_slug>/<slug:slug>/',views.product_view, name='product_view'),
]