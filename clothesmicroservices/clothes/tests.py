from django.test import TestCase
# from django.contrib.auth.models import User
from .models import Listing, Order, User, Authenticator, Address, Profile
from django.urls import reverse
# Create your tests here.

# name = models.CharField(max_length=40)
#     price = models.IntegerField()
#     color = models.CharField(max_length=15)
#     description = models.TextField()
#     seller = models.ForeignKey(User, on_delete=models.CASCADE)


#Listing tests
class GetAllListingsTestCase(TestCase):

    def setUp(self):
        test_user = User.objects.create(username='Testuser')
        test_listing1 = Listing.objects.create(
            name = "Blue shirt",
            price = 0,
            color = "Blue",
            description = "It's a blue shirt",
            seller = test_user

        )
        test_listing2 = Listing.objects.create(
            name = "Green shirt",
            price = 0,
            color = "Green",
            description = "It's a Green shirt",
            seller = test_user

        )

    def test_values(self):
        response = self.client.get(reverse('listings_list'))
        self.assertContains(response,"Green shirt")
        self.assertContains(response,"Blue shirt")
        self.assertFalse("Red shirt" in response)

class GetListingTestCase(TestCase):
    def test_success(self):
        test_user = User.objects.create(username='Testuser')
        test_listing1 = Listing.objects.create(
            name = "Blue shirt",
            price = 0,
            color = "Blue",
            description = "It's a blue shirt",
            seller = test_user
        )
        response = self.client.get(reverse('get_listing', kwargs={'listing_id':test_listing1.pk}))
        self.assertContains(response,"Blue shirt")
    def test_fail(self):
        response = self.client.get(reverse('get_listing',kwargs={'listing_id':100}))
        self.assertContains(response,'listing not found')

class NewListingTestCase(TestCase):
    def test_success(self):
        test_user = User.objects.create(username='Testuser')
        response = self.client.post(reverse('new_listing'),data={'name':'Blue Shirt',
        'price':0,
        'color': 'Blue',
        'description': 'Its not red',
        'seller_id':test_user.pk
        })
        #Response returns get from db with the new item 
        self.assertContains(response,'Blue Shirt')

    def test_fail(self):
        response = self.client.get(reverse('new_listing'))
        self.assertContains(response,'invalid')

class UpdateListingTestCase(TestCase):
    def test_success(self):
        test_user = User.objects.create(username='Testuser')
        test_listing1 = Listing.objects.create(
            name = "Green shirt",
            price = 0,
            color = "Green",
            description = "It's a Green shirt",
            seller = test_user

        )
        response = self.client.post(reverse('update_listing',kwargs={'listing_id':test_listing1.pk}), data={'name':'Blue Shirt',
        'price':0,
        'color': 'Blue',
        'description': 'Its not red',
        'seller_id':test_user.pk
        })
        #Response returns get from db with the new item 
        self.assertContains(response,'Blue Shirt')

    def test_fail(self):
        response = self.client.get(reverse('update_listing', kwargs={'listing_id':500}))
        self.assertContains(response,'not found')

class DeleteListingTestCase(TestCase):
    def test_success(self):
        test_user = User.objects.create(username='Testuser')
        test_listing1 = Listing.objects.create(
            name = "Green shirt",
            price = 0,
            color = "Green",
            description = "It's a Green shirt",
            seller = test_user

        )
        response = self.client.post(reverse('delete_listing',kwargs={'listing_id':test_listing1.pk}))
      
        self.assertContains(response,'success')


    def test_fail(self):
        response = self.client.get(reverse('delete_listing', kwargs={'listing_id':500}))
        self.assertContains(response,'not found')

#Orders tests 
# listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
#     buyer = models.ForeignKey(User, on_delete=models.CASCADE) # will not be using django users in the future
#     date = models.DateTimeField(auto_now=True)
#     deliveryMethod = models.TextField()
#     specialInstructions = models.TextField()


class GetAllOrdersTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create(username='Testuser')
        test_listing1 = Listing.objects.create(
            name = "Blue shirt",
            price = 0,
            color = "Blue",
            description = "It's a blue shirt",
            seller = test_user

        )
        test_listing2 = Listing.objects.create(
            name = "Green shirt",
            price = 0,
            color = "Green",
            description = "It's a Green shirt",
            seller = test_user

        )
        test_order1 = Order.objects.create(
            listing = test_listing1,
            buyer= test_user,
            deliveryMethod = "Pigeon",
            specialInstructions = "Don't drop it"

        )
        test_order2 = Order.objects.create(
            listing= test_listing2,
            buyer= test_user,
            deliveryMethod = "VAN",
           specialInstructions = "Don't drop it"

        )

    def test_values(self):
        response = self.client.get(reverse('orders_list'))
        self.assertContains(response,"Pigeon")
        self.assertContains(response,"VAN")

class GetOrderTestCase(TestCase):
    def test_success(self):
        test_user = User.objects.create(username='Testuser')
        test_listing1 = Listing.objects.create(
            name = "Blue shirt",
            price = 0,
            color = "Blue",
            description = "It's a blue shirt",
            seller = test_user
        )
        test_order1 = Order.objects.create(
            listing = test_listing1,
            buyer= test_user,
            deliveryMethod = "Pigeon",
            specialInstructions = "Don't drop it"

        )
        response = self.client.get(reverse('get_order',kwargs={'order_id':test_order1.pk}))
        self.assertContains(response,'Pigeon')

    def test_fail(self):
        response = self.client.get(reverse('get_order',kwargs={'order_id':100}))
        self.assertContains(response,'not found')


class NewOrderTestCase(TestCase):
    def test_success(self):
        test_user = User.objects.create(username='Testuser')
        test_listing1 = Listing.objects.create(
            name = "Blue shirt",
            price = 0,
            color = "Blue",
            description = "It's a blue shirt",
            seller = test_user

        )
        response = self.client.post(reverse('new_order'),data= {
            'listing_id': test_listing1.pk,
            'buyer_id' : test_user.pk,
            'deliveryMethod' : "Post",
            'specialInstructions': "Don't drop it"

        })

        self.assertContains(response,"Post")

    def test_fail(self):
        response = self.client.get(reverse('new_order'))
        self.assertContains(response,'invalid')

class DeleteOrderTestCase(TestCase):
    def test_fail(self):
        response = self.client.get(reverse('delete_order',kwargs={'order_id':560}))
        self.assertContains(response,'not found')
    def test_success(self):
        test_user = User.objects.create(username='Testuser')
        test_listing1 = Listing.objects.create(
            name = "Blue shirt",
            price = 0,
            color = "Blue",
            description = "It's a blue shirt",
            seller = test_user
        )
        test_order1 = Order.objects.create(
            listing = test_listing1,
            buyer= test_user,
            deliveryMethod = "Pigeon",
            specialInstructions = "Don't drop it"

        )
        response = self.client.get(reverse('delete_order',kwargs={'order_id':test_order1.pk}))
        self.assertContains(response,'success')

class UpdateOrderTestCase(TestCase):
    def test_fail(self):
        response = self.client.post(reverse('update_order',kwargs={'order_id':500}))
        self.assertContains(response,'not found')
    def test_success(self):
        test_user = User.objects.create(username='Testuser')
        test_listing1 = Listing.objects.create(
            name = "Blue shirt",
            price = 0,
            color = "Blue",
            description = "It's a blue shirt",
            seller = test_user
        )
        test_order1 = Order.objects.create(
            listing = test_listing1,
            buyer= test_user,
            deliveryMethod = "Pigeon",
            specialInstructions = "Don't drop it"

        )
        response = self.client.post(reverse('update_order',kwargs={'order_id':test_order1.pk}), data=
        {
            'deliveryMethod': "POST"
        }
        )
        self.assertContains(response,"POST")

#user-model tests
class getUserTestCase(TestCase):
    def test_fail(self):
        response = self.client.get(reverse('get_user',kwargs={'user_id':500}))
        self.assertContains(response,'not found')
    def test_success(self):
        test_user = User.objects.create(username='Testuser')
        response = self.client.get(reverse('get_user',kwargs={'user_id':test_user.pk}))
        self.assertContains(response,'Testuser')

class createAccountTestCase(TestCase):
    def test_success(self):
        response = self.client.post(reverse('create_account'),data= {
            'username': 'testusername',
            'password' : 'testpassword',
            'firstName' : 'test',
            'lastName': 'user 1', 
            'emailAddress': '123@gmail.com'
        })
        self.assertContains(response,"created")

    def test_fail(self):
        response = self.client.get(reverse('create_account'))
        self.assertContains(response,'invalid')

class createAccountTestCase2(TestCase):
    def test_success(self):
        user1 = self.client.post(reverse('create_account'),data= {
            'username': 'testusername',
            'password' : 'testpassword',
            'firstName' : 'test',
            'lastName': 'user 1', 
            'emailAddress': '123@gmail.com'
        })
        response = self.client.post(reverse('create_account'),data= {
            'username': 'testusername',
            'password' : 'testpassword',
            'firstName' : 'test',
            'lastName': 'user 1', 
            'emailAddress': '123@gmail.com'
        })
        self.assertContains(response,"already exists")

    def test_fail(self):
        response = self.client.get(reverse('create_account'))
        self.assertContains(response,'invalid')


class loginTestCase(TestCase):
    def test_success(self):
        account = self.client.post(reverse('create_account'),data= {
            'username': 'testusername',
            'password' : 'testpassword',
            'firstName' : 'test',
            'lastName': 'user 1', 
            'emailAddress': '123@gmail.com'
        })
        response = self.client.post(reverse('login'), data = {
            'username': 'testusername',
            'password' : 'testpassword',
        })
        
        self.assertContains(response,"success")

    def test_fail(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response,'invalid')


class loginTestCase2(TestCase):
    def test_success(self):
        account = self.client.post(reverse('create_account'),data= {
            'username': 'testusername',
            'password' : 'testpassword',
            'firstName' : 'test',
            'lastName': 'user 1', 
            'emailAddress': '123@gmail.com'
        })
        response = self.client.post(reverse('login'), data = {
            'username': 'testusername2',
            'password' : 'testpassword',
        })
        
        self.assertContains(response,"incorrect")

    def test_fail(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response,'invalid')
    

class loginTestCase3(TestCase):
    def test_success(self):
        account = self.client.post(reverse('create_account'),data= {
            'username': 'testusername',
            'password' : 'testpassword',
            'firstName' : 'test',
            'lastName': 'user 1', 
            'emailAddress': '123@gmail.com'
        })
        response = self.client.post(reverse('login'), data = {
            'username': 'testusername',
            'password' : 'testpassword123',
        })
        
        self.assertContains(response,"incorrect")

    def test_fail(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response,'invalid')
    

class logoutTestCase(TestCase):
    def test_success(self):
        account = self.client.post(reverse('create_account'),data= {
            'username': 'testusername',
            'password' : 'testpassword',
            'firstName' : 'test',
            'lastName': 'user 1', 
            'emailAddress': '123@gmail.com'
        })
        login = self.client.post(reverse('login'), data = {
            'username': 'testusername',
            'password' : 'testpassword',
        })
        response = self.client.post(reverse('logout'), data = {
            'username': 'testusername'
        })
        
        self.assertContains(response,"success")

    def test_fail(self):
        response = self.client.get(reverse('logout'))
        self.assertContains(response,'invalid')
    
class logoutTestCase2(TestCase):
    def test_success(self):
        account = self.client.post(reverse('create_account'),data= {
            'username': 'testusername',
            'password' : 'testpassword',
            'firstName' : 'test',
            'lastName': 'user 1', 
            'emailAddress': '123@gmail.com'
        })
        response = self.client.post(reverse('logout'), data={
            'username': 'testusername'
        })
        
        self.assertContains(response,"not logged in")

    def test_fail(self):
        response = self.client.get(reverse('logout'))
        self.assertContains(response,'invalid')

class UpdateUserTestCase(TestCase):
    def test_fail(self):
        response = self.client.get(reverse('get_user',kwargs={'user_id':500}))
        self.assertContains(response,'not found')
    def test_success(self):
        test_user = User.objects.create(username='Testuser')
        response = self.client.post(reverse('update_user',kwargs={'user_id':test_user.pk}), 
            data={'firstName':'Billy Bob'})
        self.assertContains(response,'Billy Bob')

class DeleteUserTestCase(TestCase):
    def test_fail(self):
        response = self.client.get(reverse('delete_user',kwargs={'user_id':560}))
        self.assertContains(response,'not found')
    def test_success(self):
        test_user = User.objects.create(username='Testuser')
        response = self.client.get(reverse('delete_user',kwargs={'user_id':test_user.pk}))
        self.assertContains(response,'success')

class GetAddressTestCase(TestCase):
    def test_success(self):
        test_address1 = Address.objects.create(
            street1 = "123 Street Road",
            street2 = "",
            city = "Charlottesville",
            state = "VA",
            zipCode = 22903
        )
        response = self.client.get(reverse('get_address', kwargs={'address_id':test_address1.pk}))
        self.assertContains(response,"123 Street Road")
    def test_fail(self):
        response = self.client.get(reverse('get_address',kwargs={'address_id':100}))
        self.assertContains(response,'address not found')

class NewAddressTestCase(TestCase):
    def test_success(self):
        response = self.client.post(reverse('new_address'),data={
            'street1':"123 Street Road",
            'street2':"",
            'city':"Charlottesville",
            'state':"VA",
            'zipCode':22903
        })
        #Response returns get from db with the new item 
        self.assertContains(response,'123 Street Road')

    def test_fail(self):
        response = self.client.get(reverse('new_address'))
        self.assertContains(response,'invalid')

class UpdateAddressTestCase(TestCase):
    def test_success(self):
        test_address1 = Address.objects.create(
            street1 = "123 Street Road",
            street2 = "",
            city = "Charlottesville",
            state = "VA",
            zipCode = 22903
        )
        response = self.client.post(reverse('update_address',kwargs={'address_id':test_address1.pk}), 
            data={'street1':'1234 Street Road'})
        #Response returns get from db with the new item 
        self.assertContains(response,'1234 Street Road')

    def test_fail(self):
        response = self.client.get(reverse('update_address', kwargs={'address_id':500}))
        self.assertContains(response,'not found')