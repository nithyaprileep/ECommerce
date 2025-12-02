from django.shortcuts import redirect
from Store import cart as session_cart

def add_to_cart(request, product_id):
    session_cart.add_to_cart(request.session, product_id, quantity=1)
    return redirect(request.META.get('HTTP_REFERER','/'))
