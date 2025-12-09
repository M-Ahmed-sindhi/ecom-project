from django.urls import path
from . import views

urlpatterns = [
    path('payment_success/', views.payment_success, name='payment_success'),
    path('checkout/', views.checkouts, name='checkout'),
    path('billing/', views.billing, name='billing'),
    path('process_order/', views.process_order, name='process_order'),
    path('shipped_dash/', views.shipped_dash, name='shipped_dash'),
    path('nshipped_dash/', views.nshipped_dash, name='nshipped_dash'),
     path('orders/<int:pk>', views.orders, name='orders'),
]