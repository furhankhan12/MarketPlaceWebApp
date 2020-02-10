from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Listing, Order, User
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.contrib.auth.hashers import make_password

## LISTINGS
def get_all_listings(request):
    listings = Listing.objects.all().values()
    listings_list = list(listings) 
    if listing_list:
        return JsonResponse(status=200, data=listing_list, safe=False) 
    else:
        return JsonResponse(status=404, data={'message': 'no listings'})    
   
def get_listing(request, listing_id):
    listing = Listing.objects.filter(pk=listing_id).values()
    listing_list = list(listing)
    if listing_list:
        return JsonResponse(status=200, data=listing_list, safe=False) 
    else:
        return JsonResponse(status=404, data={'error code': 404, 'message': 'listing not found', 'id searched': listing_id})    
    
    # should it be
    # if get
        # do get stuff
    # elif put
        # do put stuff
    # else
        # do get stuff
    # if that is the correct way to do it, then what is the purpose of the
    # /delete and /update urls mentioned in the project write up?
    
# new listing
def new_listing(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        color = request.POST.get('color')
        description = request.POST.get('description')
        seller = request.POST.get('seller_id')
        new_listing = Listing.objects.create(name=name, price=price, color=color, description=description, seller_id=seller)
        # listing = Listing.objects.filter(pk=new_listing.pk).values()
    
    return get_listing(request, new_listing.id)
    # if listing:
    #     return JsonResponse({'post status': 'success'})
    # else: 
    #     return JsonResponse({'post status': 'fail'})
        
# update and display listing
def update_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    print("we are inside the method")
    if request.method == "POST":
        name = request.POST.get('name')
        if name: 
            listing.name = name
        price = request.POST.get('price')
        if price:
            listing.price = price
        color = request.POST.get('color')
        if color:
            listing.color = color
        description = request.POST.get('description')
        if description:
            listing.description = description
        seller = request.POST.get('seller_id')
        if seller:
            listing.seller = seller
        listing.save()

    return get_listing(request, listing_id)
    # new_listing = Listing.objects.filter(pk=listing_id).values()
    # listing_list = list(new_listing)
    # if listing_list:
    #     return JsonResponse(status=200, data=listing_list, safe=False)

def delete_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if listing: 
        listing.delete()
        return JsonResponse({'delete status': 'success'})
    else: 
        return JsonResponse({'delete status': 'fail', 'message': 'listing not found', 'id used': listing_id})


## ORDERS
def get_all_orders(request):
    orders = Order.objects.all().values()
    orders_list = list(orders) 
    return JsonResponse(orders_list, safe=False)

def get_order(request, order_id):
    order = Order.objects.filter(pk=order_id).values()
    order_list = list(order)
    if order_list:
        return JsonResponse(status=200, data=order_list, safe=False) 
    else:
        return JsonResponse(status=404, data={'error code': 404, 'message': 'order not found', 'id searched': order_id})    
    
# new order
def new_order(request):
    if request.method == "POST":
        buyer = request.POST.get('buyer_id')
        listing = request.POST.get('listing_id')
        deliveryMethod = request.POST.get('deliveryMethod')
        specialInstructions = request.POST.get('specialInstructions')
        new_order = Order.objects.create(buyer_id=buyer, listing_id=listing, deliveryMethod=deliveryMethod, specialInstructions=specialInstructions)
        # order = Order.objects.filter(pk=new_order.pk).values()
    
    return get_order(request, new_order.id)
    # if order:
    #     return JsonResponse({'post status': 'success'})
    # else: 
    #     return JsonResponse({'post status': 'fail'})  

# update and display order
def update_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    if request.method == "POST":
        buyer = request.POST.get('buyer_id')
        if buyer:
            order.buyer = buyer
        listing = request.POST.get('listing_id')
        if listing:
            order.listing = listing    
        date = request.POST.get('date')
        if date:
            order.date = date
        deliveryMethod = request.POST.get('deliveryMethod')
        if deliveryMethod:
            order.deliveryMethod = deliveryMethod
        specialInstructions = request.POST.get('specialInstructions')
        if specialInstructions:
            order.specialInstructions = specialInstructions
        order.save()

    return get_order(request, order_id)
    # new_order = Order.objects.filter(pk=order_id).values()
    # order_list = list(new_order)
    # if order_list:
    #     return JsonResponse(status=200, data=order_list, safe=False)

# delete order
def delete_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    if order: 
        order.delete()
        return JsonResponse({'delete status': 'success'})
    else: 
        return JsonResponse({'delete status': 'fail', 'message': 'order not found', 'id used': order_id})

## USERS
def get_all_users(request):
    users = User.objects.all().values()
    users_list = list(users)
    return JsonResponse(users_list, safe=False)    

def get_user(request, user_id):
    user = User.objects.filter(pk=user_id).values()
    user_list = list(user)
    if user_list:
        return JsonResponse(status=200, data=user_list, safe=False) 
    else:
        return JsonResponse(status=404, data={'error code': 404, 'message': 'user not found', 'id searched': user_id})    
    
# new user
def new_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = make_password(request.POST.get('password'))
        new_user = User.objects.create(username=username, password=password)
        # user = User.objects.filter(pk=new_user.pk).values()
    
    return get_user(request, new_user.id)
    # if user:
    #     return JsonResponse({'post status': 'success'})
    # else: 
    #     return JsonResponse({'post status': 'fail'})  

# update and display listing
def update_user(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        if first_name:
            user.first_name = first_name
        last_name = request.POST.get('last_name')
        if last_name:
            user.last_name = last_name    
        email = request.POST.get('email')
        if email:
            user.email = email
        is_superuser = request.POST.get('is_superuser')
        if is_superuser:
            user.is_superuser = is_superuser
        is_staff = request.POST.get('is_staff')
        if is_staff:
            user.is_staff = is_staff
        user.save()

    return get_user(request, user_id)
    # new_user = User.objects.filter(pk=user_id).values()
    # user_list = list(new_user)
    # if user_list:
    #     return JsonResponse(status=200, data=user_list, safe=False)

def delete_user(request, user_id):
    user = User.objects.get(pk=user_id)
    if user: 
        user.delete()
        return JsonResponse({'delete status': 'success'})
    else: 
        return JsonResponse({'delete status': 'fail', 'message': 'user not found', 'id used': user_id})

