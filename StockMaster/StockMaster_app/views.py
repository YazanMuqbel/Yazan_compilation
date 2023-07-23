from django.shortcuts import render, redirect, reverse
from .models import *
#from .models import Product 
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse



# This function renders the homepage
def homepage(request):
    return render(request, 'homepage.html')

# This function displays all the info about a specific USER on a page with the corresponding ID
def profile(request, id):
    user = User.objects.get(id=id)
    context = {
        'user': user
    }
    return render(request, 'users-profile.html', context)

#This function renders the dashboard after the user logs in to his account
def dashboard(request):
    context = {
    'username' :  request.session['user'],
    'user' : User.objects.get(id=request.session['user'])
    }
    return render(request, 'dashboard.html', context)

#This function renders the page that displays all products in the database
def prodcuts(request):
    products = Prodcut.objects.all()
    context = {
        'products' : products
    }
    return render(request, 'products-page.html', context)

################## Registration and Loging ################
#This function renders the sign up page upon button click
def signup_page(request):
    return render(request, 'pages-register2.html')

#This function for registration process
def register(request):
    errors = User.objects.regValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/signup')
    else:
        User.objects.create(
        f_name= request.POST['f_name'], 
        l_name= request.POST['l_name'], 
        s_name= request.POST['s_name'], 
        email=request.POST['email'], 
        password=request.POST['password'])
        return render(request, 'pages-login.html')

#This function renders the Log In page upon button click
def signin_page(request):
    return render(request, 'pages-login.html')

#This function for loging process
def login(request):
    errors = User.objects.loginValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return render(request, 'pages-login.html')
    else:
        user = User.objects.get(email = request.POST['email'])
        request.session['user'] = user.id
        request.session['username'] = user.f_name
        return redirect('/dashboard')
    
# ------------------ KAREEM SECTION START ---------------------------
#Page : Order Page
def order_page(request):
    return render(request,'orders_page.html')

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

#Process: Order list
def order_list_process(request):
    print("I entered this sction")
    try:
        if is_ajax(request = request) and request.method == "POST":
            product = Prodcut.objects.get(p_barcode=request.POST['barcode'])
            print(product)
            order_list_qty = request.POST['product_qty'] 
            order_list_price = request.POST['product_price'] 
            Order_list.objects.create(p_price=order_list_price,
                                    qty_sell=order_list_qty,
                                    products=product)
            return JsonResponse({'message': 'Success'})
    except:
        return JsonResponse({'message': 'Invalid request Bro'})

def get_order_list(request):
    order_list = Order_list.objects.all().values('id','p_price', 'qty_sell', 'products__p_name', 'products__p_barcode')

    return JsonResponse({"order_list":list(order_list)})
# Process: Delete
def remove_order_list(request,order_id):
    order_list = Order_list.objects.get(id=order_id)
    order_list.delete()
    return JsonResponse({'message': 'Success'})

# ------------------ KAREEM SECTION START ---------------------------


#This function renders the "add new product" form
def add_product(request):
    return render(request, 'add_product.html')

#This function handles POST data from "add new product" form and adds new PRODUCT to db:
def save_product(request):
    if request.method == 'POST':
        params = dict()
        
        params['p_name'] = request.POST.get('p_name')
        params['p_barcode'] = request.POST.get('p_barcode')
        params['expire_date'] = request.POST.get('expire_date')
        params['cost'] = request.POST.get('cost')
        params['sale_price'] = request.POST.get('sale_price')
        params['qty'] = request.POST.get('qty')
        
        Prodcut.objects.create(**params)

    return redirect(reverse('products-page'))


