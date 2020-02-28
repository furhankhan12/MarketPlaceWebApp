from django.shortcuts import render
# import urllib
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse, HttpResponse

# Create your views here.

def get_all_listings(request):
    # note, no timeouts, error handling or all the other things needed to do this for real
    req = urllib.request.Request('http://models:8000/api/v1/listings')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    # print(resp['ok'])
    return JsonResponse(resp)


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
