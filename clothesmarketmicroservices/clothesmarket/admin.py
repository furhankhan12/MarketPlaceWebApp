from django.contrib import admin
from .models import Listing, Order, User

admin.site.register(Listing)
admin.site.register(Order)
admin.site.register(User)

# Register your models here.


