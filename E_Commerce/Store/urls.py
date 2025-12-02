from django.urls import path
from . import views

app_name = 'Store'

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/orders/', views.admin_order_list, name='admin_order_list'),
    path('admin/orders/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/orders/<int:order_id>/update/', views.admin_order_update, name='admin_order_update'),
    
    path('products/', views.admin_product_list, name='admin_product_list'),
    path('admin/products/create/', views.admin_product_create, name='admin_product_create'),
    path('admin/products/<int:pk>/edit/', views.admin_product_edit, name='admin_product_edit'),
    path('admin/products/<int:pk>/delete/', views.admin_product_delete, name='admin_product_delete'),

]
