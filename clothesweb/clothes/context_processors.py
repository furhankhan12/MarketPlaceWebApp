from django.shortcuts import render,redirect
from datetime import datetime
import urllib.request, json
import urllib.parse
from urllib.parse import urlencode
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import messages 
from django.conf import settings
from django.contrib import messages 
from django.shortcuts import get_object_or_404
from .views import get_user

# this makes it so there will always be 
# authenticated: is a user logged in?
# user: user id for the user that is logged in
# accessbile on every template

def is_authenticated(request):
    resp = get_user(request)
    if resp['ok']:
        return { 'authenticated':resp['ok'], 'user':resp['user']['id'] }
    else:
        return { 'authenticated':resp['ok'] }