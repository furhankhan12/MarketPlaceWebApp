from django.shortcuts import render,redirect
from datetime import datetime
import urllib.request, json
import urllib.parse
from urllib.parse import urlencode
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, ListingForm
from django.contrib import messages 
from django.shortcuts import get_object_or_404
# Create your views here.

def get_all_listings(request):
    # note, no timeouts, error handling or all the other things needed to do this for real
    req = urllib.request.Request('http://exp:8000/listings')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp

def home(request):
    listings_json = get_all_listings(request)
    listings_list = listings_json['listings']
  
    if listings_json['ok']:
        return render(request, 'home.html', {'listings':listings_list})
    # else:


def get_listing(request, listing_id):
    # note, no timeouts, error handling or all the other things needed to do this for real
    url = 'http://exp:8000/listings/' + str(listing_id)
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp

def update_listing(request, listing_id):
    form = ListingForm
    user = get_user_with_auth(request)
    listing = get_listing(request, listing_id)
    if user['ok'] and listing['ok']:
        user_id = user['user'][0]['id']
        seller_id = listing['listing'][0]['seller_id']
    else:
        user_id = None
        seller_id = None
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
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
            req = urllib.request.Request('http://exp:8000/listings/' + str(listing_id) + '/update')
            with urllib.request.urlopen(req,data=data) as f:
                resp = json.loads(f.read().decode('utf-8'))
                if resp['ok']==True:
                    messages.success(request, 'Listing was successfully updated.')
                    return redirect('listing', listing_id=listing_id)
                    # response = HttpResponseRedirect('/listing/' + str(listing_id))
                    # return response
                else:
                    messages.warning(request, resp['message'])   
    return render(request, 'edit_listing.html', {'form': form, 'user_id':user_id, 'seller_id':seller_id})

def delete_listing(request, listing_id):
    # note, no timeouts, error handling or all the other things needed to do this for real
    listing_data = [
        ('listing_id',listing_id),
    ]
    data = urllib.parse.urlencode(listing_data).encode("utf-8")
    req = urllib.request.Request('http://exp:8000/listings/' + str(listing_id) + '/delete')
    with urllib.request.urlopen(req,data=data) as f:
        resp_json = json.loads(f.read().decode('utf-8'))  
    if resp_json['ok']:
        # response = HttpResponseRedirect('/home')
        # return response
        messages.success(request, 'Listing was successfully deleted.')
        return redirect('home')

    else:
        messages.warning(request,resp_json['message'])
    return render(request,'home.html')   

def listing(request, listing_id):
    listing_json = get_listing(request, listing_id)
    user = get_user_with_auth(request)

    if listing_json['ok']:
        if user['ok']:
            user_id = user['user'][0]['id']
        else:
            user_id = None
        listing_list = listing_json['listing']
        return render(request, 'details.html', {'listing':listing_list, 'user_id':user_id})
    else:
        return render(request, '404_listing.html')

def get_user_with_auth(request):
    auth = request.COOKIES.get('auth') 
    if auth:
        auth_data = [
            ('auth',auth),
        ]
        data = urllib.parse.urlencode(auth_data).encode("utf-8")
        req = urllib.request.Request('http://exp:8000/users/get_user_with_auth')
        with urllib.request.urlopen(req,data=data) as f:
            resp_json = json.loads(f.read().decode('utf-8'))  
        if resp_json['ok']:
            return resp_json
        else:
            return resp_json
    else:
        resp = json.loads(json.dumps({'ok':False}))
        return resp

def new_listing(request):
    form = ListingForm()
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            seller = get_user_with_auth(request)
            if seller['ok']:
                seller_id = seller['user'][0]['id']
                listing_data = [
                    ('name',form_data['name']),
                    ('color',form_data['color']),
                    ('price', form_data['price']),
                    ('description',form_data['description']),
                    ('seller_id',seller_id)
                ]
                data = urllib.parse.urlencode(listing_data).encode("utf-8")
                req = urllib.request.Request('http://exp:8000/listings/new')
                with urllib.request.urlopen(req,data=data) as f:
                    resp = json.loads(f.read().decode('utf-8'))
                    if resp['ok']==True:
                        return redirect('listing', listing_id=resp['listing'][0]['id'])
                    else:
                        messages.warning(request, resp['message'])
        else:
            return render(request,'home.html')             
    return render(request, 'new_listing.html', {'form': form})


def search_results(request):
    current_query = str(request.GET['Query'])
    if current_query=='':
        return redirect('/home/')
    
    # query_split = current_query.split()  
    # current_query_joined = "+".join(query_split)  
    url = 'http://exp:8000/search/'+current_query
    print(url)
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    if resp!={}:
        search_list = resp['listings']
        if resp['ok']:
            print(search_list)
            return render(request, 'home.html', {'listings':search_list})
        else:
            return redirect('home')
    return render('home.html',{'listings':{}})


def create_account(request):
    form = SignUpForm()
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            account_data = [
            ('username',form_data['username']),
            ('password',form_data['password']),
            ('firstName', form_data['firstName']),
            ('lastName',form_data['lastName']),
            ('emailAddress',form_data['emailAddress']),
        ]
            # req = urllib.request.Request('http://exp:8000/users/signup',data= urllib.parse.urlencode(account_data).encode("utf-8"))
            # resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            # resp = json.loads(resp_json)
            # print(resp)
            data = urllib.parse.urlencode(account_data).encode("utf-8")
            req = urllib.request.Request('http://exp:8000/users/signup')
            with urllib.request.urlopen(req,data=data) as f:
                resp = json.loads(f.read().decode('utf-8'))
                print(resp)
                if resp['ok']==True:
                    return redirect('login')
                else:
                    messages.warning(request, resp['message'])
                
    return render(request, 'signup.html', {'form': form})

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            account_data = [
            ('username',form_data['username']),
            ('password',form_data['password']),
        ]
            data = urllib.parse.urlencode(account_data).encode("utf-8")
            req = urllib.request.Request('http://exp:8000/users/login')
            with urllib.request.urlopen(req,data=data) as f:
                resp = json.loads(f.read().decode('utf-8'))
                if resp['ok']:
                    authenticator = resp['auth']
                    response = HttpResponseRedirect('/home')
                    response.set_cookie("auth", authenticator)
                    return response
                else:
                    response = HttpResponseRedirect('/users/login')
                    messages.warning(request, resp['message'])  
                    return response 
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth = request.COOKIES.get('auth') 
    auth_data = [
        ('auth',auth),
    ]
    data = urllib.parse.urlencode(auth_data).encode("utf-8")
    req = urllib.request.Request('http://exp:8000/users/logout')
    with urllib.request.urlopen(req,data=data) as f:
        resp_json = json.loads(f.read().decode('utf-8'))  
    if resp_json['ok']:
        response = HttpResponseRedirect('/home')
        response.delete_cookie('auth')
        messages.success(request, resp_json['message'])
        return response
    else:
        messages.warning(request,resp_json['message'])
    return render(request,'home.html')





    