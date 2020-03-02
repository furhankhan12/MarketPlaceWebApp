from django.shortcuts import render,redirect
from datetime import datetime
import urllib.request, json
from django.http import JsonResponse, HttpResponse

# Create your views here.

def get_all_listings(request):
    # note, no timeouts, error handling or all the other things needed to do this for real
    req = urllib.request.Request('http://exp:8000/listings')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp

def get_listing(request, listing_id):
    # note, no timeouts, error handling or all the other things needed to do this for real
    url = 'http://exp:8000/listings/' + str(listing_id)
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp

def home(request):
    listings_json = get_all_listings(request)
    listings_list = listings_json['listings']
  
    time = datetime.now()
    if listings_json['ok']:
        return render(request, 'home.html', {'time':time, 'listings':listings_list})
    # else:

def item(request, pk):
    # time = datetime.now()
    listing_json = get_listing(request, pk)
    listing_list = listing_json['listing']
    if listing_json['ok']:
        return render(request, 'details.html', {'listing':listing_list})
def search_results(request):
    current_query = str(request.GET['Query'])
    if current_query=='':
        return redirect('/home/')
    url = 'http://exp:8000/search/'+current_query
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    if resp!={}:
        search_list = resp['listings']
        if resp['ok']:
            return render(request, 'search.html', {'listings':search_list})
        else:
            return redirect('/home/')
    return render('search.html',{'listings':{}})

    