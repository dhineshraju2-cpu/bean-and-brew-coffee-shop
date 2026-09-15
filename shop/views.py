from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import MenuItem, CartItem, Order

# Create your views here.
def home(request):
    menu_items = MenuItem.objects.filter(available=True)

    cart_count = 0

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        cart_count = sum(item.quantity for item in cart_items)

    return render(request, 'shop/home.html', {
        'menu_items': menu_items,
        'cart_count': cart_count
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')

    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
def profile(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    return render(request, 'shop/profile.html') 

def add_to_cart(request, item_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    menu_item = MenuItem.objects.get(id=item_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        menu_item=menu_item
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/#menu')      

def cart(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    cart_items = CartItem.objects.filter(user=request.user)

    total = sum(
        item.menu_item.price * item.quantity
        for item in cart_items
    )

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

def remove_from_cart(request, item_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    cart_item = CartItem.objects.filter(
        user=request.user,
        menu_item_id=item_id
    ).first()

    if cart_item:
        cart_item.delete()

    return redirect('/cart/')    

def decrease_cart(request, item_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    cart_item = CartItem.objects.filter(
        user=request.user,
        menu_item_id=item_id
    ).first()

    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('/cart/')    

def place_order(request):

    if request.method != 'POST':
        return redirect('/cart/')

    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('/cart/')

    total = sum(
        item.menu_item.price * item.quantity
        for item in cart_items
    )

    Order.objects.create(
        user=request.user,
        total_amount=total
    )

    cart_items.delete()

    return redirect('/orders/')

    

def orders(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'shop/orders.html', {
        'orders': orders
    })    


def order_detail(request, order_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    order = Order.objects.get(
        id=order_id,
        user=request.user
    )

    return render(request, 'shop/order_detail.html', {
        'order': order
    })    