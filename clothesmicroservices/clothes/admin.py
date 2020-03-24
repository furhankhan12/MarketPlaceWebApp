from django.contrib import admin
from .models import Listing, Order, User, Address, Profile, Authenticator

admin.site.register(Listing)
admin.site.register(Order)
admin.site.register(User)
admin.site.register(Address)
admin.site.register(Profile)
admin.site.register(Authenticator)

# Register your models here.


