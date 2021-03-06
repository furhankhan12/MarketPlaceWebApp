from django import forms

class SignUpForm(forms.Form):
    username = forms.CharField(label="Username", 
                                max_length=30)
    password = forms.CharField(label="Password", 
                                max_length=500, 
                                widget=forms.PasswordInput)
    firstName = forms.CharField(label="First name", 
                                max_length=30)
    lastName = forms.CharField(label="Last name", 
                                max_length=30)
    emailAddress = forms.EmailField(label="Email address", 
                                widget=forms.EmailInput)

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", max_length=500, widget=forms.PasswordInput)

class PasswordResetEmailForm(forms.Form):
    emailAddress = forms.EmailField(max_length=50)

class PassWordResetForm(forms.Form):
    new_password = forms.CharField(max_length=500,widget=forms.PasswordInput)

class UpdateUserForm(forms.Form):
    firstName = forms.CharField(label="First Name", max_length=30, required=False)
    lastName = forms.CharField(label="Last Name",max_length=30, required=False)
    emailAddress = forms.EmailField(label="Email Address", max_length=50, required=False)

class ListingForm(forms.Form):
    name = forms.CharField(label="Product name", max_length=40)
    price = forms.IntegerField(label="Price")
    color = forms.CharField(label="Color", max_length=15)
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'rows': 4}))