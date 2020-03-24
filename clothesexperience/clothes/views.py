from django.shortcuts import render
import urllib
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse, HttpResponse
import json, os, hmac
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

def get_all_listings(request):
    # note, no timeouts, error handling or all the other things needed to do this for real
    req = urllib.request.Request('http://models:8000/api/v1/listings')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    # print(resp['ok'])
    return JsonResponse(resp)

def get_listing(request, listing_id):
    # note, no timeouts, error handling or all the other things needed to do this for real
    req = urllib.request.Request('http://models:8000/api/v1/listings/' + str(listing_id))
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    # print(resp['ok'])
    return JsonResponse(resp)

def new_listing(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        color = request.POST.get('color')
        description = request.POST.get('description')
        seller_id = request.POST.get('seller_id')
        # auth = request.POST.get('auth')
        # seller = get_user_with_auth(request)
        listing_data = [
            ('name',name),
            ('price',price),
            ('color', color),
            ('description',description),
            ('seller_id',seller_id),
        ]
        data = urllib.parse.urlencode(listing_data).encode("utf-8")
        req = urllib.request.Request('http://models:8000/api/v1/listings/new')
        with urllib.request.urlopen(req,data=data) as f:
            resp_models = json.loads(f.read().decode('utf-8'))
        if resp_models['ok']:
            print(resp_models)
            # return JsonResponse(data={'ok':True, 'message': 'listing created'}) 
            return JsonResponse(data=resp_models)
        else:
            return JsonResponse(data=resp_models)


#Filter results based on what is entered in the search bar 
def get_searchResults(request, query):
    req = urllib.request.Request('http://models:8000/api/v1/listings')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    listings = resp['listings']
    return_resp = []
    for listing in listings:
        description = str(listing['description']).lower().split()
        color = str(listing['color']).lower().split()
        name = str(listing['name']).lower().split()
        to_search = " ".join([description, color, name])
        query_split = query.split()
        for search_term in query_split:
            search_term = str(search_term).lower()
            if search_term in to_search:
                return_resp.append(listing)
    resp['listings'] = return_resp
    return JsonResponse(resp)

## USERS
def get_user_with_auth(request):
    if request.method == "POST":
        auth = request.POST.get('auth')
        auth_data = [
        ('auth',auth),
        ]
        data = urllib.parse.urlencode(auth_data).encode("utf-8")
        req = urllib.request.Request('http://models:8000/api/v1/users/get_user_with_auth')
        with urllib.request.urlopen(req,data=data) as f:
            resp_json = json.loads(f.read().decode('utf-8'))  
        return JsonResponse(data = resp_json)
    # print("inside of exp, outside request")
    # print("exp", request)
    # if request.method == "GET":
    #     # auth = request.POST.get('auth')
    # # auth = request.COOKIES.get('auth')
    #     print("inside of exp")
    #     if auth:
    #         print("auth in exp", auth)
    #         url = 'http://models:8000/api/v1/users/get_user_with_auth/' + str(auth)
    #         req = urllib.request.Request(url)
    #     # print(req)
    #         resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    #         resp = json.loads(resp_json)
    #         print(resp)
    #     # return resp
    #     # data = urllib.parse.urlencode(auth).encode("utf-8")
    #     # req = urllib.request.Request('http://models:8000/api/v1/users/get_user_with_auth')

    #     # user_id = get_user_with_auth(request, auth)['user']['id']
    #     # with urllib.request.urlopen(req,data=data) as f:
    #     #     resp_models = json.loads(f.read().decode('utf-8'))
    #         if resp_json['ok']:
    #             user_id = resp_json['user']['id']
    #             return JsonResponse(data={'ok':True, 'user_id': user_id}) 
    #         else:
    #             return JsonResponse(data=resp_json)
    #     else:
    #         return JsonResponse(data={'ok':False})
    # else:
    #     return JsonResponse(data={'ok':False, 'message': 'invalid request'}) 

def create_account(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        emailAddress = request.POST.get('emailAddress')
        account_data = [
            ('username',username),
            ('password',password),
            ('firstName', firstName),
            ('lastName',lastName),
            ('emailAddress',emailAddress),
        ]
        data = urllib.parse.urlencode(account_data).encode("utf-8")
        req = urllib.request.Request('http://models:8000/api/v1/users/create_account')
        with urllib.request.urlopen(req,data=data) as f:
            resp_models = json.loads(f.read().decode('utf-8'))
        if resp_models['ok']:
                return JsonResponse(data={'ok':True, 'message': 'account created'}) 
        else:
            return JsonResponse(data=resp_models)

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        account_data = [
            ('username',username),
            ('password',password),
        ]
        data = urllib.parse.urlencode(account_data).encode("utf-8")
        req = urllib.request.Request('http://models:8000/api/v1/users/login')
        with urllib.request.urlopen(req,data=data) as f:
            resp_json = json.loads(f.read().decode('utf-8'))  
        return JsonResponse(data = resp_json)

def logout(request):
    if request.method == "POST":
        auth = request.POST.get('auth')
        auth_data = [
        ('auth',auth),
        ]
        data = urllib.parse.urlencode(auth_data).encode("utf-8")
        req = urllib.request.Request('http://models:8000/api/v1/users/logout')
        with urllib.request.urlopen(req,data=data) as f:
            resp_json = json.loads(f.read().decode('utf-8'))  
        return JsonResponse(data = resp_json)
    else:
        return JsonResponse(data={'ok':False, 'message': 'Invalid request'}) 




# make a POST request.
# we urlencode the dictionary of values we're passing up and then make the POST request
# again, no error handling

# print('About to perform the POST request...')

# post_data = {'title': 'Demo Post', 'body': 'This is a test', 'userId': 1}

# post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

# req = urllib.request.Request('http://placeholder.com/v1/api/posts/create', data=post_encoded, method='POST')
# resp_json = urllib.request.urlopen(req).read().decode('utf-8')

# resp = json.loads(resp_json)
# print(resp)
