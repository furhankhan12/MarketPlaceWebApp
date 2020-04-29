from django.shortcuts import render
import urllib
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse, HttpResponse
import json, os, hmac
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from kafka import KafkaProducer
from elasticsearch import Elasticsearch 
import time

sleep_time = 2
retries = 5
for x in range(0, retries):  
    try:
        producer = KafkaProducer(bootstrap_servers=['kafka:9092'])
        es = Elasticsearch(['es'])        
        strerror = None
    except:
        strerror = "error"
        pass

    if strerror:
        print("exp: sleeping for", sleep_time)
        time.sleep(sleep_time)
        sleep_time *= 2
    else:
        break

def get_all_listings(request):
    # note, no timeouts, error handling or all the other things needed to do this for real
    req = urllib.request.Request('http://models:8000/api/v1/listings')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)

def get_listing(request, listing_id):
    # note, no timeouts, error handling or all the other things needed to do this for real
    req = urllib.request.Request('http://models:8000/api/v1/listings/' + str(listing_id))
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    user_id = request.POST.get('user_id')
    if resp['ok'] and user_id and producer:
        # producer = KafkaProducer(bootstrap_servers=['kafka:9092'])
        listing = {'user_id': user_id, 'item_id':str(listing_id)}
        # print("HAVE A NEW ITEM TO TRACK")
        producer.send('track-views-topic', json.dumps(listing).encode('utf-8'))
        print("HAVE A NEW ITEM TO TRACK")
    if resp['ok']:
        return JsonResponse(resp)

def update_listing(request, listing_id):
# note, no timeouts, error handling or all the other things needed to do this for real
   if request.method == "POST":
        name = request.POST.get('name')
        color = request.POST.get('color')
        price = request.POST.get('price')
        description = request.POST.get('description')
        listing_data = [
            ('name',name),
            ('color',color),
            ('price',price),
            ('description',description),
        ]
        data = urllib.parse.urlencode(listing_data).encode("utf-8")
        req = urllib.request.Request('http://models:8000/api/v1/listings/' + str(listing_id) + '/update')
        with urllib.request.urlopen(req,data=data) as f:
            resp_models = json.loads(f.read().decode('utf-8'))
        if resp_models['ok']:
            print(resp_models) 
            return JsonResponse(data=resp_models)
        else:
            return JsonResponse(data=resp_models)  

def delete_listing(request, listing_id):
    if request.method == "POST":
        listing_data = [
            ('listing_id',listing_id),
        ]
        data = urllib.parse.urlencode(listing_data).encode("utf-8")
        req = urllib.request.Request('http://models:8000/api/v1/listings/' + str(listing_id) + '/delete')
        with urllib.request.urlopen(req,data=data) as f:
            resp_json = json.loads(f.read().decode('utf-8'))  
        if es:
            es.delete('listing_index', doc_type='listing',id=listing_id)
        return JsonResponse(data = resp_json)
    else:
        return JsonResponse(data={'ok':False, 'message': 'invalid request'})        

def new_listing(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        color = request.POST.get('color')
        description = request.POST.get('description')
        seller_id = request.POST.get('seller_id')
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
            listing = resp_models['listing'][0]
            if producer:
                producer.send('new-listings-topic', json.dumps(listing).encode('utf-8'))
            return JsonResponse(data=resp_models)
        else:
            return JsonResponse(data=resp_models)

#Filter results based on what is entered in the search bar 
def get_searchResults(request, query):

    if es:
        new_query = query.replace('___',' ')
        search = es.search(index='listing_index', body={'query': {'query_string': {'query': new_query}}})
        # list of results
        res = search['hits']['hits']
        listings = []
        print(res)
        for x in res:
            listings.append({'listing':x['_source'], 'score':x['_score']})
        print(listings)
        return JsonResponse(data={'ok':True, 'listings':listings})
    else:
        return JsonResponse(data={'ok':False, 'message': 'Failed to connect to search engine. Please try again at another time.'})

def get_most_popular(request, query):
    if es:
        #3 underscores ___
        new_query = query.replace("___"," ")
        # score based off of visits, sorted is descending order, top 6
        search = es.search(index='listing_index', body={'sort': [{'visits': 'desc'}],'size': 6,'query': {'function_score': {'query': {'query_string': {'query': new_query}},'field_value_factor': {'field': 'visits','modifier': 'log1p','missing': 0}}}})
        res = search['hits']['hits']
        listings = []
        for x in res:
            listings.append({'listing':x['_source'], 'score':x['_score']})
        print(listings)
        return JsonResponse(data={'ok':True, 'listings':listings})
    else:
        return JsonResponse(data={'ok':False, 'message': 'Failed to connect to search engine. Please try again at another time.'})


## USERS
def get_user(request):
    if request.method == "POST":
        auth = request.POST.get('auth')
        auth_data = [
            ('auth',auth)
        ]
        data = urllib.parse.urlencode(auth_data).encode("utf-8")
        req = urllib.request.Request('http://models:8000/api/v1/users/get_user')
        with urllib.request.urlopen(req,data=data) as f:
            resp_json = json.loads(f.read().decode('utf-8'))  
        if resp_json['ok']:
            return JsonResponse(data=resp_json)
        else:
            return JsonResponse(data={'ok':False, 'message': 'invalid request'}) 
    else:
        return JsonResponse(data={'ok':False, 'message': 'invalid request'}) 

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

def update_user_profile(request):
    if request.method == "POST":
        auth_token = request.POST.get('auth')
        emailAddress = request.POST.get('emailAddress')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        update_data = [
            ('emailAddress',emailAddress),
            ('firstName',firstName),
            ('lastName',lastName),
            ('auth',auth_token),
        ]
        data = urllib.parse.urlencode(update_data).encode("utf-8")
        req = urllib.request.Request('http://models:8000/api/v1/users/update_information')
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
