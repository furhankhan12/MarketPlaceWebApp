from django import forms
class SignUpForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=500,widget=forms.PasswordInput)
    firstName = forms.CharField(max_length=30)
    lastName = forms.CharField(max_length=30)
    emailAddress = forms.EmailField(max_length=50)
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=500,widget=forms.PasswordInput)
class PasswordResetEmailForm(forms.Form):
    emailAddress = forms.EmailField(max_length=50)
class PassWordResetForm(forms.Form):
    new_password = forms.CharField(max_length=500,widget=forms.PasswordInput)
class UpdateUserForm(forms.Form):
    firstName = forms.CharField(max_length=30, required=False)
    lastName = forms.CharField(max_length=30, required=False)
    emailAddress = forms.EmailField(max_length=50, required=False)



