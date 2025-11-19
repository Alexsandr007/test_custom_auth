from django.urls import path
from .views import ProductListView, OrderListView, StoreListView

app_name = 'business'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('stores/', StoreListView.as_view(), name='store-list'),
]