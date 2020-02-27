from django.shortcuts import render
# import urllib
import urllib.request
import json
from django.http import JsonResponse, HttpResponse

# Create your views here.

def get_all_listings(request):
    # url = "http://localhost:8001/api/v1/listings"
    # webURL = urllib.request.urlopen(url)
    # data = webURL.read()
    # JSON_object = json.loads(data.decode('utf-8'))
    req = urllib.request.Request('http://localhost:8001/api/v1/listings')
    # print(req)
    # res = urllib.request.urlopen(req)
    # req = urllib.request.urlopen('http://models:8000/api/v1/listings')
    # print(res)
    return req
