from django.shortcuts import render
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

def home(request):
    listings_json = get_all_listings(request)
    # listings_list = json.dumps(listings_json['listings'])
    listings_list = listings_json['listings']
    # listings = list(listings_list)
    print(listings_json)
    time = datetime.now()
    # if 'ok':'true',
    return render(request, 'home.html', {'time':time, 'range':range(5), 'listings':listings_list})


def item(request, pk):
    # time = datetime.now()
    return render(request, 'details.html', {'pk':pk})