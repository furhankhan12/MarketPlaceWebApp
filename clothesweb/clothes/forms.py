from django import forms
class SignUpForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=500,widget=forms.PasswordInput)
    firstName = forms.CharField(max_length=30)
    lastName = forms.CharField(max_length=30)
    emailAddress = forms.CharField(max_length=50)
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=500,widget=forms.PasswordInput)


