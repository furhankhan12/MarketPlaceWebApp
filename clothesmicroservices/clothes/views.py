from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Listing, Order, User
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.contrib.auth.hashers import make_password
import json

## LISTINGS
def get_all_listings(request):
    listings = Listing.objects.all().values()
    listings_list = list(listings) 
    listings_dict = {'ok':True, 'listings': listings_list}
    if listings_dict:
        return JsonResponse(data=listings_dict) 
    else:
        return JsonResponse(data={'ok':False, 'message': 'listings not found'})    

 #Get a specific listing  
def get_listing(request, listing_id):
    listing = Listing.objects.filter(pk=listing_id).values()
    listing_list = list(listing)
    listing_dict = {'ok':True, 'listing': listing_list}
    if listing_list:
        return JsonResponse(data=listing_dict) 
    else:
        return JsonResponse(data={'ok':False, 'message': 'listing not found', 'id searched': listing_id})    
    
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
        # output after create
        return get_listing(request, new_listing.id)
    else:
        return JsonResponse(data={'ok':False, 'message': 'invalid request'})  
    
        
# update and display listing
def update_listing(request, listing_id):
    try: 
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist: 
        listing = None
    
    if not listing: 
        return JsonResponse(data={'ok':False,'message': 'listing not found', 'id searched': listing_id})    
    else:
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
                listing.seller_id = seller
            listing.save()
            return get_listing(request, listing_id)
        else:
            return JsonResponse(data={'ok':False, 'message': 'invalid request'})    

    # output after update
   

#delete a specfic listing
def delete_listing(request, listing_id):
    try: 
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist: 
        listing = None
    
    if not listing: 
        return JsonResponse(data={'ok':False,'message': 'listing not found', 'id searched': listing_id, 'delete status': 'failure'})    
    else:
        listing.delete()
        return JsonResponse({'ok':True,'delete status': 'success'})

## ORDERS
def get_all_orders(request):
    orders = Order.objects.all().values()
    orders_list = list(orders) 
    orders_dict = {'ok':True, 'orders': orders_list}
    if orders_dict:
        return JsonResponse(data=orders_dict) 
    else:
        return JsonResponse(data={'ok':False, 'message': 'orders not found'}) 

#return order with a pk
def get_order(request, order_id):
    order = Order.objects.filter(pk=order_id).values()
    order_list = list(order)
    order_dict = {'ok':True, 'order': order_list}
    if order_list:
        return JsonResponse(data=order_dict) 
    else:
        return JsonResponse( data={'ok':False, 'message': 'order not found', 'id searched': order_id})    
    
# new order
def new_order(request):
    if request.method == "POST":
        buyer = request.POST.get('buyer_id')
        listing = request.POST.get('listing_id')
        deliveryMethod = request.POST.get('deliveryMethod')
        specialInstructions = request.POST.get('specialInstructions')
        new_order = Order.objects.create(buyer_id=buyer, listing_id=listing, deliveryMethod=deliveryMethod, specialInstructions=specialInstructions)
        # return after creating
        return get_order(request, new_order.id)
    else:
        return JsonResponse(data={'ok':False, 'message': 'invalid request'})    


# update and display order
def update_order(request, order_id):
    try: 
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist: 
        order = None

    if not order:
        return JsonResponse( data={'ok':False,  'message': 'order not found', 'id searched': order_id})        
    else:
        if request.method == "POST":
            buyer = request.POST.get('buyer_id')
            if buyer:
                order.buyer_id = buyer
            listing = request.POST.get('listing_id')
            if listing:
                order.listing_id = listing    
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
            # output after update    
            return get_order(request, order_id)
        else:
            return JsonResponse(data={'ok':False, 'message': 'invalid request'})    
    

# delete order
def delete_order(request, order_id):
    try: 
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist: 
        order = None

    if not order:
        return JsonResponse(data={'ok':False, 'message': 'order not found', 'id searched': order_id, 'delete status': 'failure'})        
    else:
        order.delete()
        return JsonResponse({'ok':True, 'delete status': 'success'})

## USERS
def get_all_users(request):
    users = User.objects.all().values()
    users_list = list(users)
    users_dict = {'ok':True, 'users': users_list}
    if users_dict:
        return JsonResponse(data=users_dict) 
    else:
        return JsonResponse(data={'ok':False, 'message': 'users not found'})  

def get_user(request, user_id):
    user = User.objects.filter(pk=user_id).values()
    user_list = list(user)
    user_dict = {'ok':True, 'user': user_list}
    if user_list:
        return JsonResponse(data=user_list) 
    else:
        return JsonResponse(data={'ok': False, 'message': 'user not found', 'id searched': user_id})    
    
# new user
def new_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = make_password(request.POST.get('password'))
        new_user = User.objects.create(username=username, password=password)
        # output after create
        return get_user(request, new_user.id)
    else:
        return JsonResponse(data={'ok':False, 'message': 'invalid request'})   

# update and display listing
def update_user(request, user_id):
    try: 
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist: 
        user = None

    if not user:
        return JsonResponse(data={'ok': False, 'message': 'user not found', 'id searched': user_id})        
    else:
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
            # output after update
            return get_user(request, user_id)
        else:
            return JsonResponse(data={'ok':False, 'message': 'invalid request'})    

#delete users
def delete_user(request, user_id):
    try: 
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist: 
        user = None

    if not user:
        return JsonResponse(data={'ok':False,'message': 'user not found', 'id searched': user_id, 'delete status': 'failure'})        
    else:
        user.delete()
        return JsonResponse({'ok':True, 'delete status': 'success'})

