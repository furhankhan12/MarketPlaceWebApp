from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Listing, Order, User, Authenticator, Profile, Address
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.contrib.auth.hashers import make_password, check_password
import json, os, hmac
from django.conf import settings
import urllib

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
        return JsonResponse(data={'ok':True, 'delete status': 'success'})



# def get_all_users(request):
#     users = User.objects.all().values()
#     users_list = list(users)
#     users_dict = {'ok':True, 'users': users_list}
#     if users_dict:
#         return JsonResponse(data=users_dict) 
#     else:
#         return JsonResponse(data={'ok':False, 'message': 'users not found'})  

def get_user(request, user_id):
    user = User.objects.filter(pk=user_id).values()
    user_list = list(user)
    user_dict = {'ok':True, 'user': user_list}
    if user_list:
        return JsonResponse(data=user_dict) 
    else:
        return JsonResponse(data={'ok': False, 'message': 'user not found', 'id searched': user_id})    

# def get_user_username(request, user_name):
#     user = User.objects.filter(username=user_name).first()
#     if user is None:
#         return JsonResponse(data={'ok': False, 'message': 'user not found', 'user_name searched': user_name}) 
#     else:
#         user_list = list(user)
#         user_dict = {'ok':True, 'user': user_list}
#         return JsonResponse(data=user_dict) 
        
def create_account(request):
    if request.method == "POST":
        salt = hmac.new(
                key = settings.SECRET_KEY.encode('utf-8'),
                msg = os.urandom(32),
                digestmod = 'sha256',
            ).hexdigest()
        username = request.POST.get('username')
        password = make_password(request.POST.get('password'), salt=salt)
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        emailAddress = request.POST.get('emailAddress')

        user = User.objects.filter(username=username).first()
        user_email = User.objects.filter(emailAddress=emailAddress).first()
        if not user and not user_email:
            new_user = User.objects.create(username=username, password=password, firstName=firstName, lastName=lastName, emailAddress=emailAddress)
        # output after create
        # login(request)
            return JsonResponse(data={'ok':True, 'message': 'account created'}) 
        if user:
            return JsonResponse(data={'ok':False, 'message': 'username already exists'}) 
        if user_email:
            return JsonResponse(data={'ok':False, 'message': 'email already in use'}) 

    else:
        return JsonResponse(data={'ok':False, 'message': 'invalid request'})   

    
# new user
# username = models.CharField(max_length=30, unique=True)
#     password = models.CharField(max_length=500)
#     firstName = models.CharField(max_length=30)
#     lastName = models.CharField(max_length=30)
#     emailAddress = models.CharField(max_length=50, unique=True)
# def new_user(request):
#     if request.method == "POST":
#         # resp_json= urllib.request.urlopen(request.POST).read().decode('utf-8')
#         # resp = json.loads(resp_json)
#         # username = resp['username']
#         # password = resp['password']
#         # firstName = resp['firstName']
#         # lastName = resp['lastName']
#         # emailAddress = resp['emailAddress']
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         firstName = request.POST.get('firstName')
#         lastName = request.POST.get('lastName')
#         emailAddress = request.POST.get('emailAddress')
#         new_user = User.objects.create(username=username, password=password, firstName = firstName,
#          lastName = lastName, emailAddress=emailAddress)
#         # output after create
#         return JsonResponse(data={'ok':True, 'message': 'New account created'})
         
    

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()
        if user:
            valid = check_password(password, user.password)
            if valid:
                authenticator = hmac.new(
                    key = settings.SECRET_KEY.encode('utf-8'),
                    msg = os.urandom(32),
                    digestmod = 'sha256',
                ).hexdigest()
                # user_id = user.id
                auth = Authenticator.objects.create(user_id=user, authenticator=authenticator)
                return JsonResponse(data={'ok':True, 'auth': auth.authenticator, 'login status': 'success'})
            else: 
                return JsonResponse(data={'ok':False, 'login status': 'incorrect username or password'})
        else:
            return JsonResponse(data={'ok':False, 'message': 'incorrect username or password'})
    else:
        return JsonResponse(data={'ok':False, 'message': 'invalid request'})       

def logout(request):
    if request.method == "POST":
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        auth = Authenticator.objects.filter(user_id=user).first()

        if not auth:
            return JsonResponse(data={'ok':False, 'message': 'not logged in', 'logout status': 'failure'})
        else: 
            auth.delete()
            return JsonResponse(data={'ok':True, 'logout status': 'success'})
    else:
        return JsonResponse(data={'ok':False, 'message': 'invalid request'})   
    

# def get_all_users(request):
#     users = User.objects.all().values()
#     users_list = list(users)
#     users_dict = {'ok':True, 'users': users_list}
#     if users_dict:
#         return JsonResponse(data=users_dict) 
#     else:
#         return JsonResponse(data={'ok':False, 'message': 'users not found'})  

def get_user(request, user_id):
    user = User.objects.filter(pk=user_id).values()
    user_list = list(user)
    user_dict = {'ok':True, 'user': user_list}
    if user_list:
        return JsonResponse(data=user_dict) 
    else:
        return JsonResponse(data={'ok': False, 'message': 'user not found', 'id searched': user_id})    
       
# update and display user
def update_user(request, user_id):
    try: 
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist: 
        user = None

    if not user:
        return JsonResponse(data={'ok': False, 'message': 'user not found', 'id searched': user_id})        
    else:
        if request.method == "POST":
            firstName = request.POST.get('firstName')
            if firstName:
                user.firstName = firstName
            lastName = request.POST.get('lastName')
            if lastName:
                user.lastName = lastName    
            emailAddress = request.POST.get('emailAddress')
            if emailAddress:
                user.emailAddress = emailAddress
            user.save()
            # output after update
            return get_user(request, user_id)
        else:
            return JsonResponse(data={'ok':False, 'message': 'invalid request'})    

# delete user
def delete_user(request, user_id):
    try: 
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist: 
        user = None

    if not user:
        return JsonResponse(data={'ok':False,'message': 'user not found', 'id searched': user_id, 'delete status': 'failure'})        
    else:
        logout(request)
        user.delete()
        return JsonResponse({'ok':True, 'delete status': 'success'})

## ADDRESS
# new address
def new_address(request):
    if request.method == "POST":
        street1 = request.POST.get('street1')
        street2 = request.POST.get('street2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipCode = request.POST.get('zipCode')
        new_address = Address.objects.create(street1=street1, street2=street2, city=city, state=state, zipCode=zipCode)
        # output after create
        return get_address(request, new_address.id)
    else:
        return JsonResponse(data={'ok':False, 'message': 'invalid request'})  

# get address
def get_address(request, address_id):
    address = Address.objects.filter(pk=address_id).values()
    address_list = list(address)
    address_dict = {'ok':True, 'address': address_list}
    if address_list:
        return JsonResponse(data=address_dict) 
    else:
        return JsonResponse(data={'ok':False, 'message': 'address not found', 'id searched': address_id})     

# update and display address
def update_address(request, address_id):
    try: 
        address = Address.objects.get(pk=address_id)
    except Address.DoesNotExist: 
        address = None
    
    if not address: 
        return JsonResponse(data={'ok':False,'message': 'address not found', 'id searched': address_id})    
    else:
        if request.method == "POST":
            street1 = request.POST.get('street1')
            if street1:
                address.street1 = street1
            street2 = request.POST.get('street2')
            if street2:
                address.street2 = street2
            city = request.POST.get('city')
            if city:
                address.city = city
            state = request.POST.get('state')
            if state:
                address.state = state
            zipCode = request.POST.get('zipCode')
            if zipCode:
                address.zipCode = zipCode
            address.save()
            return get_address(request, address_id)
        else:
            return JsonResponse(data={'ok':False, 'message': 'invalid request'})    

## PROFILES
# new profile
def new_profile(request, user_id):
    try: 
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist: 
        user = None

    if not user:
        return JsonResponse(data={'ok': False, 'message': 'user not found', 'id searched': user_id})        
    else:
        if request.method == "POST":
            shippingAddress = request.POST.get('shippingAddress')
            phoneNumber = request.POST.get('phoneNumber')
            profile = Profile.objects.create(user=user, shippingAddress=shippingAddress, phoneNumber=phoneNumber)
            # return after creating
            return get_order(request, new_order.id)
        else:
            return JsonResponse(data={'ok':False, 'message': 'invalid request'})

# get profile
def get_profile(request, profile_id):
    profile = Profile.objects.filter(pk=profile_id).values()
    profile_list = list(profile)
    profile_dict = {'ok':True, 'profile': profile_list}
    if profile_list:
        return JsonResponse(data=profile_dict) 
    else:
        return JsonResponse(data={'ok':False, 'message': 'profile not found', 'id searched': profile_id})     

# update and display profile
def update_profile(request, profile_id):
    try: 
        profile = Profile.objects.get(pk=profile_id)
    except Profile.DoesNotExist: 
        profile = None
    
    if not profile: 
        return JsonResponse(data={'ok':False,'message': 'address not found', 'id searched': profile_id})    
    else:
        if request.method == "POST":
            shippingAddress = request.POST.get('shippingAddress')
            if shippingAddress:
                profile.shippingAddress = shippingAddress
            phoneNumber = request.POST.get('phoneNumber')
            if phoneNumber:
                profile.phoneNumber = phoneNumber
            profile.save()
            return get_address(request, profile_id)
        else:
            return JsonResponse(data={'ok':False, 'message': 'invalid request'})    
