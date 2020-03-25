from django.shortcuts import render,redirect
from datetime import datetime
import urllib.request, json
import urllib.parse
from urllib.parse import urlencode
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PasswordResetEmailForm, PassWordResetForm, UpdateUserForm
from django.contrib import messages 
from django.core.mail import send_mail
from django.conf import settings

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

# def home(request):
#     listings_json = get_all_listings(request)
#     listings_list = listings_json['listings']
  
#     if listings_json['ok']:
#         return render(request, 'home.html', {'listings':listings_list})
#     # else:


def get_listing(request, listing_id):
    # note, no timeouts, error handling or all the other things needed to do this for real
    url = 'http://exp:8000/listings/' + str(listing_id)
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp
def get_user(request):
    if request.COOKIES.get('auth'):
        auth = request.COOKIES.get('auth') 
        auth_data = [
        ('auth',auth),
        ]
        data = urllib.parse.urlencode(auth_data).encode("utf-8")
        req = urllib.request.Request('http://exp:8000/users/get_user')
        with urllib.request.urlopen(req,data=data) as f:
            resp_json = json.loads(f.read().decode('utf-8'))  
        if resp_json['ok']:
            return resp_json
    return {'ok':False}


def home(request):
    listings_json = get_all_listings(request)
    listings_list = listings_json['listings']
    authenticated = False
    if request.COOKIES.get('auth'):
        authenticated=True
    user_info = get_user(request)
    time = datetime.now()
    if listings_json['ok'] and user_info['ok']:
        return render(request, 'home.html', {'time':time, 'listings':listings_list, 'authenticated':authenticated, 'user_info':user_info['user']})
    if listings_json['ok']:
        return render(request, 'home.html', {'time':time, 'listings':listings_list, 'authenticated':authenticated})

def item(request, pk):
    # time = datetime.now()
    listing_json = get_listing(request, pk)
    listing_list = listing_json['listing']
    authenticated = False
    if request.COOKIES.get('auth'):
        authenticated=True
    if listing_json['ok']:
        return render(request, 'details.html', {'listing':listing_list, 'authenticated':authenticated})

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
    authenticated = False
    if request.COOKIES.get('auth'):
        authenticated=True
    if resp!={}:
        search_list = resp['listings']
        if resp['ok']:

            return render(request, 'search.html', {'listings':search_list, 'authenticated':authenticated})

            # print(search_list)
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
                # print(resp)
                if resp['ok']==True:
                    subject = 'Thank you for registering to our site'
                    message = ' it  means the world to us '
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [form_data['emailAddress'],]
                    send_mail( subject, message, email_from, recipient_list )
                    messages.success(request,"Account Created")
                    return redirect('/users/login')
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
            if resp['ok']==True:
                authenticator = resp['auth']
                response = HttpResponseRedirect('/home')
                response.set_cookie("auth", authenticator)
                # print(resp)
                return response
            else:
                messages.error(request, resp['message'])
        
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

def reset_password_email(request):
    form = PasswordResetEmailForm()
    if request.method == 'POST':
        form = PasswordResetEmailForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            email_data = [
            ('emailAddress',form_data['emailAddress']),
        ]
            data = urllib.parse.urlencode(email_data).encode("utf-8")
            req = urllib.request.Request('http://exp:8000/users/reset_password_email')
            with urllib.request.urlopen(req,data=data) as f:
                resp = json.loads(f.read().decode('utf-8'))
                if resp['ok']==True:
                    subject = 'Your Reset Token'
                    message = "http://localhost:8000/users/reset_password/"+str(resp['token'])
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [form_data['emailAddress'],]
                    send_mail( subject, message, email_from, recipient_list )
                    messages.success(request, "Email has been sent")
                    return redirect("/home")
                else:
                    messages.error(request, resp['message']) 
    return render(request, 'reset_password_email.html', {'form': form})
def reset_password(request,token):
    
    form = PassWordResetForm()
    if request.method == 'POST':
        form = PassWordResetForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            password_data = [
            ('new_password',form_data['new_password']),
            ('token',token),
        ]
            data = urllib.parse.urlencode(password_data).encode("utf-8")
            req = urllib.request.Request('http://exp:8000/users/reset_password')
            with urllib.request.urlopen(req,data=data) as f:
                resp = json.loads(f.read().decode('utf-8'))
                if resp['ok']==True:
                    messages.success(request,"Password has been reset")
                    return redirect("/home")
                else:
                    messages.error(request, resp['message']) 
    return render(request, 'reset_password.html', {'form': form})

def update_user_profile(request):
    form = UpdateUserForm()
    if request.method == 'POST':
        auth = request.COOKIES.get('auth') 
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            updated_data = [
            ('lastName',form_data['lastName']),
            ('firstName',form_data['firstName']),
            ('emailAddress',form_data['emailAddress']),
            ('auth',auth),
        ]
            if not form_data['lastName']and not form_data['firstName'] and not form_data['emailAddress'] :
                messages.error(request,"No changes applied")
                return redirect("/home")
            data = urllib.parse.urlencode(updated_data).encode("utf-8")
            req = urllib.request.Request('http://exp:8000/users/update_information')
            with urllib.request.urlopen(req,data=data) as f:
                resp = json.loads(f.read().decode('utf-8'))
                if resp['ok']==True:
                    messages.success(request,"Profile has been updated")
                    return redirect("/home")
                else:
                    messages.error(request, resp['message']) 
    return render(request, 'update_user.html', {'form': form}) 






    





    