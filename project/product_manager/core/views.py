from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction, DatabaseError

# Tumhare Models aur Forms yahan import ho rahe hain
from .models import Product, CartItem, Specification
from .forms import ProductForm, SpecificationFormSet

# 1. Product List (Home)
@login_required
def product_list(request):
    try:
        products = Product.objects.all()
        return render(request, 'core/product_list.html', {'products': products})
    except DatabaseError as e:
        messages.error(request, f"Database Error: {e}")
        return render(request, 'core/product_list.html', {'products': []})

# 2. Product Detail
@login_required
def product_detail(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)
        return render(request, 'core/product_detail.html', {'product': product})
    except Exception as e:
        messages.error(request, "Product not found or error occurred.")
        return redirect('product_list')

# 3. Product Create
@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = SpecificationFormSet(request.POST)
        
        try:
            if form.is_valid() and formset.is_valid():
                with transaction.atomic():
                    product = form.save()
                    formset.instance = product
                    formset.save()
                    messages.success(request, "Product created successfully!")
                    return redirect('product_list')
            else:
                messages.error(request, "Please correct the errors below.")
        except Exception as e:
            messages.error(request, f"System Error: {str(e)}")
    else:
        form = ProductForm()
        formset = SpecificationFormSet()
    
    return render(request, 'core/product_form.html', {'form': form, 'formset': formset, 'action': 'Create'})

# 4. Product Update
@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = SpecificationFormSet(request.POST, instance=product)
        
        try:
            if form.is_valid() and formset.is_valid():
                with transaction.atomic():
                    form.save()
                    formset.save()
                    messages.success(request, "Product updated!")
                    return redirect('product_detail', pk=product.pk)
        except Exception as e:
            messages.error(request, f"Update Failed: {e}")
    else:
        form = ProductForm(instance=product)
        formset = SpecificationFormSet(instance=product)

    return render(request, 'core/product_form.html', {'form': form, 'formset': formset, 'action': 'Edit'})

# 5. Product Delete
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    try:
        product.delete()
        messages.success(request, "Product deleted!")
    except Exception as e:
        messages.error(request, f"Could not delete: {e}")
    return redirect('product_list')

# ---------------------------------------------------
# CART FUNCTIONALITY (Yahan hai tumhara Cart Code)
# ---------------------------------------------------

# 6. Add to Cart
# core/views.py mein is function ko replace karo

@login_required
# core/views.py

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # --- Try-Except Block (Interview ke liye) ---
    try:
        # URL se quantity nikalo (e.g. ?qty=2)
        qty = int(request.GET.get('qty', 1))
        
        # Agar quantity 1 se kam hai to error maano
        if qty < 1:
            raise ValueError("Quantity cannot be less than 1")
            
    except ValueError:
        # Agar user ne 'ABC' ya '-5' likha to ye chalega
        qty = 1
        messages.warning(request, "⚠️ Invalid Quantity! Defaulted to 1.")
        print(f"--- EXCEPTION HANDLED: Invalid input for {product.name} ---")

    # --- Main Cart Logic ---
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        # AGAR PEHLE SE HAI: To purani quantity mein nayi jod do
        cart_item.quantity += qty
        messages.success(request, f"Added {qty} more {product.name}(s)! Total: {cart_item.quantity}")
    else:
        # AGAR NAYA HAI: To quantity set kar do
        cart_item.quantity = qty
        messages.success(request, f"Added {qty} x {product.name} to cart!")
    
    # Save karna mat bhoolna!
    cart_item.save()
    
    return redirect('product_list')

# 7. View Cart
@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    
    # Total Price Calculation
    # Hum yahan seedha logic laga rahe hain taaki agar Model mein function na ho tab bhi code chale
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    return render(request, 'core/cart.html', {'cart_items': cart_items, 'total_price': total_price})

# 8. Remove from Cart
@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('view_cart')