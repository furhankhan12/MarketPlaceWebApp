from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    price = models.IntegerField()
    color = models.CharField(max_length=15)
    description = models.TextField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE) # will not be using django users in the future

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE) # will not be using django users in the future
    date = models.DateTimeField(auto_now=True)
    deliveryMethod = models.TextField()
    specialInstructions = models.TextField()

# other things that could be modeled
# - more specific delivery method
# - addresses for users
# - users

# other things are could be generated in the views, but may not need models
# - order history
# - listing history
