from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns =[
    path('signup/',views.signup,name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name='userprofile/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('myaccount/',views.myaccount,name='myaccount'),
    path('mystore/',views.my_store,name='mystore'),
    path("mystore/order_detail/<int:pk>/",views.my_store_order_detail,name="order_detail"),
    path("mystore/add_product/",views.add_product,name='add_product'),
    path("mystore/edit_product/<int:product_id>/",views.edit_product,name='edit_product'),
    path('mystore/delete_product/<int:product_id>/',views.delete_product,name='delete_product'),
    path('vendor/<int:pk>/',views.vendor_detail,name='vendor_detail'),

    
   
]
    