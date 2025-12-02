from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from Cart.models import *
from django.contrib import messages
from .forms import ProductForm

def home(request):
    return render(request, 'Store/base_admin.html')

@staff_member_required
def admin_order_list(request): #admin can view user placed oreders
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'Store/admin_order_list.html', {'orders': orders})

@staff_member_required
def admin_order_detail(request, order_id): #user wise order
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'Store/admin_order_detail.html', {'order': order})

@staff_member_required
def admin_order_update(request, order_id): #admin can update order status
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.status = request.POST.get('status', order.status)
        order.save()
        return redirect('Store:admin_order_detail', order_id=order.id)
    #return render(request, 'Store/admin_order_update.html', {'order': order})
    return render(request, 'Store/admin_order_edit.html', {'order': order})

@staff_member_required
def admin_product_list(request): 
    products = Product_Table.objects.all().order_by('-id')
    return render(request, "Store/admin_product_list.html", {"products": products})

@staff_member_required
def admin_product_create(request): #add or Edit products
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect("Store:admin_product_list")
    else:
        form = ProductForm()
    return render(request, "Store/admin_product_edit.html", {"form": form})

@staff_member_required
def admin_product_edit(request, pk): #edit products
    product = get_object_or_404(Product_Table, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('Store:admin_product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'Store/admin_product_edit.html', {'form': form, 'product': product})

@staff_member_required
def admin_product_delete(request, pk): #delete products
    product = get_object_or_404(Product_Table, pk=pk)
    product.delete()
    messages.warning(request, f"Product '{product.name}' has been deleted!")
    return redirect('Store:admin_product_list')
