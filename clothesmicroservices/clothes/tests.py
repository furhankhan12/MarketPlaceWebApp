from django.test import TestCase
# from django.contrib.auth.models import User
from .models import Listing, Order, User, Authenticator, Address, Profile
from django.urls import reverse
import json
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


class getUserTestCase(TestCase):
    def test_fail(self):
        response = self.client.get(reverse('get_user_id',kwargs={'user_id':500}))
        self.assertContains(response,'not found')
    def test_success(self):
        test_user = User.objects.create(username='Testuser')
        response = self.client.get(reverse('get_user_id',kwargs={'user_id':test_user.pk}))
        self.assertContains(response,'Testuser')


# class getUserTestCase2(TestCase):
#     def test_fail(self):
#         response = self.client.get(reverse('get_user_auth',kwargs={'auth':500}))
#         self.assertContains(response,'not found')
#     def test_success(self):
#         account = self.client.post(reverse('create_account'),data= {
#             'username': 'testusername',
#             'password' : 'testpassword',
#             'firstName' : 'test',
#             'lastName': 'user 1', 
#             'emailAddress': '123@gmail.com'
#         })
#         login = self.client.post(reverse('login'), data = {
#             'username': 'testusername',
#             'password' : 'testpassword',
#         })
#         response = self.client.get(reverse('get_user_auth',kwargs={'auth':login.json()['auth']}))
#         self.assertContains(response,'testusername')

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


# class loginTestCase2(TestCase):
#     def test_success(self):
#         account = self.client.post(reverse('create_account'),data= {
#             'username': 'testusername',
#             'password' : 'testpassword',
#             'firstName' : 'test',
#             'lastName': 'user 1', 
#             'emailAddress': '123@gmail.com'
#         })
#         response = self.client.post(reverse('login'), data = {
#             'username': 'testusername2',
#             'password' : 'testpassword',
#         })
        
#         self.assertContains(response,"incorrect")

#     def test_fail(self):
#         response = self.client.get(reverse('login'))
#         self.assertContains(response,'invalid')
    

# class loginTestCase3(TestCase):
#     def test_success(self):
#         account = self.client.post(reverse('create_account'),data= {
#             'username': 'testusername',
#             'password' : 'testpassword',
#             'firstName' : 'test',
#             'lastName': 'user 1', 
#             'emailAddress': '123@gmail.com'
#         })
#         response = self.client.post(reverse('login'), data = {
#             'username': 'testusername',
#             'password' : 'testpassword123',
#         })
        
#         self.assertContains(response,"incorrect")

#     def test_fail(self):
#         response = self.client.get(reverse('login'))
#         self.assertContains(response,'invalid')
    

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
        json_login = json.loads(str(login.content, encoding='utf8'))
       
        response = self.client.post(reverse('logout'), data = {
            'auth': json_login['auth'],
        })

        response_json = json.loads(str(response.content, encoding='utf8'))
        
        self.assertEquals(response_json['message'],"Successfully logged out.")

    def test_fail(self):
        response = self.client.get(reverse('logout'))
      
        self.assertContains(response,'invalid')

# class logoutTestCase2(TestCase):
#     def test_success(self):
#         account = self.client.post(reverse('create_account'),data= {
#             'username': 'testusername',
#             'password' : 'testpassword',
#             'firstName' : 'test',
#             'lastName': 'user 1', 
#             'emailAddress': '123@gmail.com'
#         })
#         response = self.client.post(reverse('logout'), data={
#             'username': 'testusername'
#         })
        
#         self.assertContains(response,"not logged in")

#     def test_fail(self):
#         response = self.client.get(reverse('logout'))
#         self.assertContains(response,'invalid')

class UpdateUserTestCase(TestCase):
    def test_fail(self):
        response = self.client.get(reverse('update_user',kwargs={'user_id':500}))
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


class GetProfileTestCase(TestCase):
    def test_success(self):
        test_user1 = User.objects.create(
            username= 'testusername',
            password = 'testpassword',
            firstName = 'test',
            lastName = 'user 1', 
            emailAddress = '123@gmail.com'
        )
        test_address1 = Address.objects.create(
            street1 = "123 Street Road",
            street2 = "",
            city = "Charlottesville",
            state = "VA",
            zipCode = 22903
        )
        test_profile1 = Profile.objects.create(
            user = test_user1,
            shippingAddress = test_address1, 
            phoneNumber = '123-1234-1234'
        )
        response = self.client.get(reverse('get_profile', kwargs={'profile_id':test_profile1.pk}))
        self.assertContains(response,"123-1234-1234")
    def test_fail(self):
        response = self.client.get(reverse('get_profile',kwargs={'profile_id':100}))
        self.assertContains(response,'profile not found')

class NewProfileTestCase(TestCase):
    def test_success(self):
        test_user1 = User.objects.create(
            username= 'testusername',
            password = 'testpassword',
            firstName = 'test',
            lastName = 'user 1', 
            emailAddress = '123@gmail.com'
        )
        test_address1 = Address.objects.create(
            street1 = "123 Street Road",
            street2 = "",
            city = "Charlottesville",
            state = "VA",
            zipCode = 22903
        )
        response = self.client.post(reverse('new_profile', kwargs={'user_id':test_user1.pk}),
            data={
                'user_id':test_user1.pk,
                'shippingAddress_id':test_address1.pk,
                'phoneNumber':"123-1234-1234"
            })
        #Response returns get from db with the new item 
        self.assertContains(response,'123-1234-1234')

    def test_fail(self):
        response = self.client.get(reverse('new_profile', kwargs={'user_id':500}))
        self.assertContains(response,'user not found')

class UpdateProfileTestCase(TestCase):
    def test_success(self):
        test_user1 = User.objects.create(
            username= 'testusername',
            password = 'testpassword',
            firstName = 'test',
            lastName = 'user 1', 
            emailAddress = '123@gmail.com'
        )
        test_address1 = Address.objects.create(
            street1 = "123 Street Road",
            street2 = "",
            city = "Charlottesville",
            state = "VA",
            zipCode = 22903
        )
        test_profile1 = Profile.objects.create(
            user_id = test_user1.pk,
            shippingAddress_id = test_address1.pk,
            phoneNumber = "123-1234-1234"
        )
        response = self.client.post(reverse('update_profile',kwargs={'profile_id':test_profile1.pk}), 
            data={'phoneNumber':'234-2345-2345'})
        #Response returns get from db with the new item 
        self.assertContains(response,'234-2345-2345')


class getUserTestCase(TestCase):

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
        json_login = json.loads(str(login.content, encoding='utf8'))
       
        response_get = self.client.post(reverse('get_user'), data = {
            'auth': json_login['auth'],
        })
        
        response_json = json.loads(str(response_get.content, encoding='utf8'))

        self.assertDictEqual(response_json,{'ok': True, 'user': {'First Name': 'test', 'Email Address': '123@gmail.com', 'Last Name': 'user 1'}})


    def test_fail(self):
        response = self.client.get(reverse('get_user'))
        self.assertContains(response,'invalid')

class ChangeUserPasswordTestCase(TestCase):

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
        json_login = json.loads(str(login.content, encoding='utf8'))
       
        response_token = self.client.post(reverse('generate_token'), data = {
            'emailAddress' : '123@gmail.com',
        })
        json_token = json.loads(str(response_token.content, encoding='utf8'))
        token = str(json_token['token'])
        reset_password = self.client.post(reverse('reset_password'), data = {
            'token' : token,
            'new_password':'Hi'
        })
        new_login = self.client.post(reverse('login'), data = {
            'username': 'testusername',
            'password' : 'Hi',
        })
        new_login_json = json.loads(str(new_login.content, encoding='utf8'))
        self.assertEquals(new_login_json['login status'],'success')


    def test_fail(self):
        response = self.client.get(reverse('get_user'))
        self.assertContains(response,'invalid')

class UpdateUserProfileTestCase(TestCase):

    def test_fail(self):
        response = self.client.get(reverse('update_user_profile'))
        self.assertContains(response,'invalid')


    

    def test_fail(self):
        response = self.client.get(reverse('update_profile', kwargs={'profile_id':500}))
        self.assertContains(response,'not found')

class UpdateProfileTestCase2(TestCase):
    def test_success(self):
        test_user1 = User.objects.create(
            username= 'testusername',
            password = 'testpassword',
            firstName = 'test',
            lastName = 'user 1', 
            emailAddress = '123@gmail.com'
        )
        test_address1 = Address.objects.create(
            street1 = "123 Street Road",
            street2 = "",
            city = "Charlottesville",
            state = "VA",
            zipCode = 22903
        )
        test_profile1 = Profile.objects.create(
            user_id = test_user1.pk,
            shippingAddress_id = test_address1.pk,
            phoneNumber = "123-1234-1234"
        )

        test_address2 = Address.objects.create(
            street1 = "234 Street Road",
            street2 = "",
            city = "Charlottesville",
            state = "VA",
            zipCode = 22903
        )

        response = self.client.post(reverse('update_profile',kwargs={'profile_id':test_profile1.pk}), 
            data={'shippingAddress_id':test_address2.pk})
        #Response returns get from db with the new item 
        self.assertContains(response,test_address2.pk)

    def test_fail(self):
        response = self.client.get(reverse('update_profile', kwargs={'profile_id':500}))
        self.assertContains(response,'not found')