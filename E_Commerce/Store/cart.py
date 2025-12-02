CART_SESSION_ID = 'cart'
RECENTLY_VIEWED_ID = 'recently_viewed'
MAX_RECENT = 10

def _get_cart(session):
    return session.get(CART_SESSION_ID, {})

def save_cart(session, cart):
    session[CART_SESSION_ID] = cart
    session.modified = True

def add_to_cart(session, product_id, quantity=1):
    cart = _get_cart(session)
    pid = str(product_id)
    cart[pid] = cart.get(pid, 0) + int(quantity)
    save_cart(session, cart)

def remove_from_cart(session, product_id):
    cart = _get_cart(session)
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
    save_cart(session, cart)

def update_cart_item(session, product_id, quantity):
    cart = _get_cart(session)
    pid = str(product_id)
    if int(quantity) <= 0:
        cart.pop(pid, None)
    else:
        cart[pid] = int(quantity)
    save_cart(session, cart)

def clear_cart(session):
    session.pop(CART_SESSION_ID, None)
    session.modified = True

def get_cart_items(session):
    return _get_cart(session)

def add_recently_viewed(session, product_id):
    recent = session.get(RECENTLY_VIEWED_ID, [])
    pid = str(product_id)
    if pid in recent:
        recent.remove(pid)
    recent.insert(0, pid)
    session[RECENTLY_VIEWED_ID] = recent[:MAX_RECENT]
    session.modified = True

def get_recently_viewed(session):
    return session.get(RECENTLY_VIEWED_ID, [])
