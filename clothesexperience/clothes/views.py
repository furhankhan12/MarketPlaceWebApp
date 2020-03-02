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
