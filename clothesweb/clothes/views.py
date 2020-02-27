from django.shortcuts import render
from datetime import datetime

# Create your views here.

def home(request):
    time = datetime.now()
    return render(request, 'home.html', {'time':time, 'range':range(5)})


def item(request, pk):
    # time = datetime.now()
    return render(request, 'details.html', {'pk':pk})