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

#Filter results based on what is entered in the search bar 
def get_searchResults(request, query):
    req = urllib.request.Request('http://models:8000/api/v1/listings')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    listings = resp['listings']
    return_resp = []
    for listing in listings:
        description = str(listing['description']).lower().split()
        query_split = query.split()
        for search_term in query_split:
            search_term = str(search_term).lower()
            if search_term in description:
                return_resp.append(listing)
    resp['listings'] = return_resp
    return JsonResponse(resp)


## USERS
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
        return JsonResponse(data={'ok':True, 'message': 'Invalid request'}) 

def reset_password(request):
    if request.method == "POST":
        token = request.POST.get('token')
        new_password = request.POST.get('new_password')
        auth_data = [
        ('token',token),
        ('new_password',new_password),
        ]
        data = urllib.parse.urlencode(auth_data).encode("utf-8")
        req = urllib.request.Request('http://models:8000/api/v1/users/reset_password')
        with urllib.request.urlopen(req,data=data) as f:
            resp_json = json.loads(f.read().decode('utf-8'))  
        return JsonResponse(data = resp_json)
    else:
        return JsonResponse(data={'ok':True, 'message': 'Invalid request'})

def reset_password_email(request):
    if request.method == "POST":
        email = request.POST.get('emailAddress')
        email_data = [
            ('emailAddress',email),
        ]
        data = urllib.parse.urlencode(email_data).encode("utf-8")
        req = urllib.request.Request('http://models:8000/api/v1/users/generate_token')
        with urllib.request.urlopen(req,data=data) as f:
            resp_json = json.loads(f.read().decode('utf-8'))  
        return JsonResponse(data = resp_json)
    else:
        return JsonResponse(data={'ok':True, 'message': 'Invalid request'})

        












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
