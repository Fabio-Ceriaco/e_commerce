from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms
from .models import Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=100)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UpdateUserForm(UserChangeForm):
    email = forms.EmailField(required=False, max_length=100)
    password = None # hidden password
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        
class ChangePasswordFrom(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
        
class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(max_length=10)
    address1 = forms.CharField(max_length=200)
    address2 = forms.CharField(max_length=200)
    city = forms.CharField(max_length=200)
    zipcode = forms.CharField(max_length=200)
    country = forms.CharField(max_length=200)
    
    class Meta:
        model = Profile
        fields = ['phone', 'address1', 'address2', 'zipcode', 'city', 'country']
        
            