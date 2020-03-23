from django.db import models
import datetime
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=500)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    emailAddress = models.CharField(max_length=50, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('emailAddress',)

class Authenticator(models.Model):
    authenticator = models.CharField(primary_key=True, max_length=64)
    user_id = models.IntegerField()
    date_created = models.DateTimeField(auto_now=True)

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    street1 = models.CharField(max_length=40)
    street2 = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=2)
    zipCode = models.IntegerField()

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shippingAddress = models.OneToOneField(Address, on_delete=models.CASCADE)
    phoneNumber = models.CharField(max_length=13)

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    price = models.IntegerField()
    color = models.CharField(max_length=15)
    description = models.TextField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
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
