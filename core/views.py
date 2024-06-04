from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import * 
from .forms import CreateUserForm
import json
import datetime
from .guest import cartData, guestOrder

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateUserForm
from .models import Customer

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create Customer object associated with the user
            customer = Customer(user=user)
            customer.save()

            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            return redirect('login')
        else:
            # If form is invalid, handle error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    context = {'form': form}
    return render(request, 'core/register.html', context)




def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Check if the customer exists, if not, create one
            if not hasattr(user, 'customer'):
                customer = Customer(user=user)
                customer.save()

            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect')

    context = {}
    return render(request, 'core/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

def rewardpage(request):
	context = {}
	return render( request, 'core/rewards.html', context)

def wheelpage(request):
	context = {}
	return render( request, 'core/wheel.html', context)

def aboutuspage(request):
	context = {}
	return render( request, 'core/aboutus.html', context)





def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems': cartItems}
	return render(request, 'core/store.html', context)

def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
		


	context = {'items':items, 'order': order, 'cartItems': cartItems}
	return render(request, 'core/cart.html', context)
  

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order': order, 'cartItems': cartItems}
	return render(request, 'core/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']  #we access it now as its now dictionary
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
# add or remove the item 
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()
# to remove the item when there is no quantity
	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

def home(request):
    return render(request, 'core/home.html')