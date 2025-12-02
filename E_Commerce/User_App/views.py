from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from Cart.models import *
from Store import cart as session_cart
from .forms import RegisterForm, LoginForm, UserForm, UserProfileForm
from .models import UserProfile




def home(request):  #For all users
    return render(request, 'base.html')

def product_list(request): #List of products for users
    qs = Product_Table.objects.all().order_by('-created_at')
    return render(request, 'User_App/product_list.html', {'products': qs})

def product_detail(request, pk): #detailed view
    product = get_object_or_404(Product_Table, pk=pk)
    session_cart.add_recently_viewed(request.session, product.pk)
    return render(request, 'User_App/product_detail.html', {'product': product})


@login_required 
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    items = CartItem.objects.filter(cart=cart)

    total = sum(item.product.price * item.quantity for item in items)

    return render(request, "User_App/cart.html", {
        "items": items,
        "total": total,
    })
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('User_App:cart_view')

def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity"))

        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()

    return redirect('User_App:cart_view')

@login_required
def checkout(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    items = CartItem.objects.filter(cart=cart)

    total = sum(item.subtotal() for item in items)

    if request.method == "POST":
        # Create Order
        order = Order.objects.create(
            user=user,
            total_amount=total
        )

        # Create Order Items
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_purchase=item.product.price
            )

        # Clear Cart
        items.delete()

        messages.success(request, "Order placed successfully!")
        return redirect("User_App:dashboard")

    return render(request, 'User_App/checkout.html', {
        "items": items,
        "total": total
    })
@login_required
def order_history(request): #history of orders
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'User_App/orders.html', {'orders': orders})

@login_required
def order_detail(request, pk): #each items detail
    order = get_object_or_404(Order, pk=pk, user=request.user)
    items = OrderItem.objects.filter(order=order)
    return render(request, 'User_App/order_detail.html', {'order': order, 'items': items})

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # ADMIN CHECK — is_superuser or is_staff
            if user.is_superuser or user.is_staff:
                return redirect("Store:home")

            # NORMAL USER
            return redirect("User_App:dashboard")

        else:
            messages.error(request, "Invalid username or password")
            return redirect("User_App:login")

    return render(request, "User_App/login.html")

def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out.')
    return redirect('User_App:login')

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('User_App:product_list')
    else:
        form = RegisterForm()
    return render(request, 'User_App/register.html', {'form': form})

@login_required
def profile_view(request): #user profile view of registered user
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'User_App/profile.html', {'profile': profile})

@login_required
def profile_edit(request): #profile edit
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated.')
            return redirect('User_App:profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    return render(request, 'User_App/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def recently_viewed(request): #recently detailed viwed product using session
    ids = session_cart.get_recently_viewed(request.session)
    products = Product_Table.objects.filter(pk__in=[int(i) for i in ids])
    ordered = sorted(products, key=lambda p: ids.index(str(p.pk)))
    return render(request, 'User_App/recent.html', {'products': ordered})

@login_required
def dashboard(request): #registered user dashboard
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    recent_orders = orders[:5]  # last 5 orders
    total_orders = orders.count()
    total_spent = sum(order.total_amount for order in orders)

    context = {
        'user': user,
        'orders': recent_orders,
        'total_orders': total_orders,
        'total_spent': total_spent,
    }
    return render(request, 'User_App/dashboard.html', context)

@login_required
def add_to_cart(request, product_id): #user can add products to cart
    product = Product_Table.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key or request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        item.quantity += 1

    item.save()

    return redirect("User_App:product_list")
    

