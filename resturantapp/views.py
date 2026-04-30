from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Address, MenuItem, Order, OrderItem, Review, CartItem
import json

def reservation(request):
    return render(request, 'reservation.html')

def dashboard(request):
    return render(request, 'dashboard.html')
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_reservations.html', {'reservations': reservations})
# ─── Home / Index ────────────────────────────────────────────────
@login_required(login_url='login')
def index(request):
    if request.method == "POST":
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        phone   = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()
        if not all([name, email, phone, message]):
            messages.error(request, "All fields are required.")
            return redirect('index')
        Address.objects.create(name=name, email=email, phone=phone, message=message)
        messages.success(request, "Message sent successfully! We'll get back to you soon.")
        return redirect('index')

    top_items = MenuItem.objects.filter(is_available=True).order_by('-created_at')[:6]
    reviews   = Review.objects.filter(is_approved=True).select_related('user').order_by('-created_at')[:5]
    cart_count = CartItem.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    return render(request, 'index.html', {
        'top_items': top_items,
        'reviews': reviews,
        'cart_count': cart_count,
    })


# ─── Menu ────────────────────────────────────────────────────────
def menu(request):
    category = request.GET.get('category', 'all')
    items = MenuItem.objects.filter(is_available=True)
    if category != 'all':
        items = items.filter(category=category)
    categories = MenuItem.CATEGORY_CHOICES
    cart_count = CartItem.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    return render(request, 'menu.html', {
        'menu_items': items,
        'categories': categories,
        'current_category': category,
        'cart_count': cart_count,
    })


# ─── Static Pages ────────────────────────────────────────────────
def services(request):
    return render(request, 'services.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


# ─── Auth: Register ──────────────────────────────────────────────
def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        username   = request.POST.get('username', '').strip()
        email      = request.POST.get('email', '').strip()
        password   = request.POST.get('password', '')
        password1  = request.POST.get('password1', '')

        if not all([first_name, last_name, username, email, password, password1]):
            messages.error(request, "All fields are required.")
            return redirect('register')

        if password != password1:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose another.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect('register')

        try:
            validate_password(password)
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            login(request, user)
            messages.success(request, f"Welcome to MOMOS, {first_name}! 🎉")
            return redirect('index')
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return redirect('register')

    return render(request, 'auth/register.html')


# ─── Auth: Login ─────────────────────────────────────────────────
def log_in(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, "Both username and password are required.")
            return render(request, 'auth/login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next', 'index')
            return redirect(next_url)
        messages.error(request, "Invalid username or password. Please try again.")
    return render(request, 'auth/login.html')


# ─── Auth: Logout ────────────────────────────────────────────────
@login_required(login_url='login')
def log_out(request):
    logout(request)
    messages.success(request, "Logged out successfully. See you soon!")
    return redirect('login')


# ─── Cart ────────────────────────────────────────────────────────
@login_required(login_url='login')
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('item')
    total = sum(ci.item.price * ci.quantity for ci in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


@login_required(login_url='login')
@require_POST
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id, is_available=True)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    cart_count = CartItem.objects.filter(user=request.user).count()
    return JsonResponse({'success': True, 'cart_count': cart_count, 'message': f'{item.name} added to cart!'})


@login_required(login_url='login')
@require_POST
def remove_from_cart(request, item_id):
    CartItem.objects.filter(user=request.user, item_id=item_id).delete()
    cart_items = CartItem.objects.filter(user=request.user).select_related('item')
    total = sum(ci.item.price * ci.quantity for ci in cart_items)
    cart_count = cart_items.count()
    return JsonResponse({'success': True, 'cart_count': cart_count, 'total': str(total)})


@login_required(login_url='login')
@require_POST
def update_cart(request, item_id):
    data = json.loads(request.body)
    qty = int(data.get('quantity', 1))
    if qty < 1:
        CartItem.objects.filter(user=request.user, item_id=item_id).delete()
    else:
        CartItem.objects.filter(user=request.user, item_id=item_id).update(quantity=qty)
    cart_items = CartItem.objects.filter(user=request.user).select_related('item')
    total = sum(ci.item.price * ci.quantity for ci in cart_items)
    return JsonResponse({'success': True, 'total': str(total)})


# ─── Orders ──────────────────────────────────────────────────────
@login_required(login_url='login')
@require_POST
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('item')
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    total = sum(ci.item.price * ci.quantity for ci in cart_items)
    order = Order.objects.create(user=request.user, total_price=total)
    for ci in cart_items:
        OrderItem.objects.create(order=order, item=ci.item, quantity=ci.quantity, price=ci.item.price)
    cart_items.delete()
    messages.success(request, f"Order #{order.id} placed successfully! Total: रु{total}")
    return redirect('order_history')


@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__item').order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})


# ─── Reviews ─────────────────────────────────────────────────────
@login_required(login_url='login')
@require_POST
def add_review(request):
    name    = request.POST.get('reviewer_name', request.user.get_full_name() or request.user.username)
    rating  = int(request.POST.get('rating', 5))
    comment = request.POST.get('comment', '').strip()
    if comment:
        Review.objects.create(user=request.user, reviewer_name=name, rating=rating, comment=comment)
        messages.success(request, "Thank you for your review!")
    else:
        messages.error(request, "Review cannot be empty.")
    return redirect('index')


# ─── Profile ─────────────────────────────────────────────────────
@login_required(login_url='login')
def profile(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name).strip()
        user.last_name  = request.POST.get('last_name', user.last_name).strip()
        user.email      = request.POST.get('email', user.email).strip()
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'profile.html', {'orders': orders})


# ── ADD THIS TO YOUR views.py ──────────────────────────────────────────────
# (Paste inside views.py alongside the other view functions)

def cart(request):
    """
    Cart page — cart items are stored client-side in localStorage.
    This view just renders the template; JS handles all cart logic.
    If the user submits the checkout form (POST), it creates an Order.
    """
    if request.method == "POST":
        import json
        from .models import Order, OrderItem, MenuItem

        if not request.user.is_authenticated:
            messages.error(request, "Please log in to place an order.")
            return redirect('login')

        try:
            cart_data   = json.loads(request.POST.get('cart_data', '[]'))
            order_type  = request.POST.get('order_type', 'dine_in')
            delivery_addr = request.POST.get('delivery_address', '')
        except (json.JSONDecodeError, ValueError):
            messages.error(request, "Invalid cart data. Please try again.")
            return redirect('cart')

        if not cart_data:
            messages.error(request, "Your cart is empty.")
            return redirect('cart')

        order = Order.objects.create(
            user=request.user,
            order_type=order_type,
            delivery_address=delivery_addr,
            status='placed',
        )

        for item in cart_data:
            try:
                menu_item = MenuItem.objects.get(pk=item['id'])
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=item['qty'],
                    unit_price=menu_item.price,
                )
            except (MenuItem.DoesNotExist, KeyError):
                continue  # skip invalid items

        order.calculate_total()
        messages.success(request, f"Order #{order.pk} placed successfully! We'll prepare it right away.")
        return redirect('index')

    return render(request, 'cart.html')

