from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Listing, Order, User
from django.shortcuts import get_object_or_404
from django.core import serializers

def get_all_listings(request):
    listings = Listing.objects.all().values()
    listings_list = list(listings) 
    return JsonResponse(status=200, data=listings_list, safe=False)
   
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
        listing = Listing.objects.filter(pk=new_listing.pk).values()
    
    if listing:
        return JsonResponse({'post status': 'success'})
    else: 
        return JsonResponse({'post status': 'fail'})
        
# update listing
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

    new_listing = Listing.objects.filter(pk=listing_id).values()
    listing_list = list(new_listing)
    if listing_list:
        return JsonResponse(status=200, data=listing_list, safe=False)

def delete_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if listing: 
        listing.delete()
        return JsonResponse({'delete status': 'success'})
    else: 
        return JsonResponse({'delete status': 'fail', 'reason':'listing does not exist'})

def get_all_orders(request):
    orders = Order.objects.all().values()
    orders_list = list(orders) 
    return JsonResponse(orders_list, safe=False)

def get_all_users(request):
    users = User.objects.all().values()
    users_list = list(users)
    return JsonResponse(users_list, safe=False)    

# def get_order(request):
#     orders = Order.objects.all().values()
#     orders_list = list(orders)  # important: convert the QuerySet to a list object
#     return JsonResponse(orders_list, safe=False)

# def put_order(request):
#     orders = Order.objects.all().values()
#     orders_list = list(orders)  # important: convert the QuerySet to a list object
#     return JsonResponse(orders_list, safe=False)

# def delete_order(request):
#     orders = Order.objects.all().values()
#     orders_list = list(orders)  # important: convert the QuerySet to a list object
#     return JsonResponse(orders_list, safe=False)

# def update_order(render):    
