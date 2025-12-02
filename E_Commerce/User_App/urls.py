from django.urls import path
from .import views
app_name = 'User_App'
urlpatterns = [
    path('product_list', views.product_list, name='product_list'),
    path('home/', views.home, name='home'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
     path("update_cart/<int:item_id>/", views.update_cart, name="update_cart"),
    path("remove_cart_item/<int:item_id>/", views.remove_cart_item, name="remove_cart_item"),

    # path('login/', views.login_user, name='login'),
    path('', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('recent/', views.recently_viewed, name='recent'),
   
   

   
    path('update/<int:item_id>/', views.update_cart, name='update_cart'),
   
    path('remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
]



