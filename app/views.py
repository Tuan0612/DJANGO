from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db.models import Sum

# Create your views here.
def about(request):
    return render(request, 'app/about.html')
def confirm_payment(request):
    # Xử lý xác nhận thanh toán ở đây
    # Sau khi xử lý thành công, chuyển hướng đến trang "Home"
    return redirect('app/home.html')  # 'home' là tên của đường dẫn đến trang "Home" trong urls.py của bạn
def payment(request):
    if request.method == "POST":
        # Lấy thông tin từ POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        country = request.POST.get('country')
        payment_method = request.POST.get('method')
        
        # Bạn có thể xử lý thêm dữ liệu ở đây, ví dụ lưu vào database
        
        # Chuyển dữ liệu đến template thanh toán
        context = {
            'name': name,
            'email': email,
            'address': address,
            'city': city,
            'state': state,
            'zipcode': zipcode,
            'country': country,
            'payment_method': payment_method,
        }
        return render(request, 'app/payment.html', context)
    else:
        # Nếu không phải là POST request, redirect về form hoặc trang chủ
        return redirect('app/home.html')  # Giả sử 'home' là name của URL trang chủ  

def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = False
    else:
        items = []
        cartItems = 0
        user_not_login = True
    id=request.GET.get('id','')
    products = Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub=False)
    context = {'productS':products,'categories':categories,'items': items, 'order': order, 'cartItems': cartItems, 'user_not_login': user_not_login}
    return render(request, 'app/detail.html', context)


def category(request):
    categories = Category.objects.filter(is_sub=False)
    active_category_slug = request.GET.get('category', '')
    if active_category_slug:
        try:
            active_category = Category.objects.get(slug=active_category_slug)
            products = Product.objects.filter(category=active_category)

            # Tính toán số lượng sản phẩm trong giỏ hàng cho mỗi sản phẩm
            if request.user.is_authenticated:
                customer = request.user
                order, created = Order.objects.get_or_create(customer=customer, complete=False)
                cart_items = order.orderitem_set.aggregate(total_items=Sum('quantity'))['total_items'] or 0
                for product in products:
                    product.cart_quantity = order.orderitem_set.filter(product=product).aggregate(total_items=Sum('quantity'))['total_items'] or 0
        except Category.DoesNotExist:
            active_category = None
            products = None
    else:
        active_category = None
        products = Product.objects.all()

        # Tính toán số lượng sản phẩm trong giỏ hàng cho mỗi sản phẩm
        if request.user.is_authenticated:
            customer = request.user
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            cart_items = order.orderitem_set.aggregate(total_items=Sum('quantity'))['total_items'] or 0
            for product in products:
                product.cart_quantity = order.orderitem_set.filter(product=product).aggregate(total_items=Sum('quantity'))['total_items'] or 0

    context = {'categories': categories, 'active_category': active_category, 'products': products, 'cartItems': cart_items}
    return render(request, 'app/category.html', context)

def search(request):
    if request.method == "POST":
        searched = request.POST.get("searched", "")
        keys = Product.objects.filter(name__icontains=searched)
    else:
        keys = []
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        cartItems = 0
    products = Product.objects.all()
    return render(request, 'app/search.html', {"searched": searched, "keys": keys, "products": products, "cartItems": cartItems})

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, 'app/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect!')
    return render(request, 'app/login.html')

def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
        user_not_login = False
    else:
        cartItems = 0
        user_not_login = True
    categories = Category.objects.filter(is_sub=False)
    products = Product.objects.all()
    context = {'categories': categories, 'products': products, 'cartItems': cartItems, 'user_not_login': user_not_login}
    return render(request, 'app/home.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = False
    else:
        items = []
        cartItems = 0
        user_not_login = True
    categories = Category.objects.filter(is_sub=False)
    context = {'categories':categories,'items': items, 'order': order, 'cartItems': cartItems, 'user_not_login': user_not_login}
    return render(request, 'app/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = False
    else:
        items = []
        cartItems = 0
        user_not_login = True
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'user_not_login': user_not_login}
    return render(request, 'app/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item updated', safe=False)
