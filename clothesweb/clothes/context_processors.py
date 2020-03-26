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
        return {'ok':False}

def is_authenticated(request):
    resp = get_user_with_auth(request)
    return { 'authenicated':resp['ok'] }