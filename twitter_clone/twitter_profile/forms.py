# Import django forms and models
from PIL import Image
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.html import strip_tags
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from .models import TwitterProfile

class PersonalInfoForm(forms.Form):
    banner_picture = forms.ImageField(required=False,label="",widget=forms.FileInput(attrs={'accept': 'image/*', '@change':'onBannerChange', 'class':'btn btn-primary'}))
    profile_picture = forms.ImageField(required=False,label="",widget=forms.FileInput(attrs={'accept': 'image/*', '@change':'onProfileChange', 'class':'btn btn-primary'}))
    username = forms.CharField(label="", max_length=50, widget=forms.widgets.TextInput(attrs={':maxlength':'max_user', 'v-model':'username','placeholder': 'Add your name', 'class': 'form-control', '@focus':'user_focus = true', '@blur':'user_focus = false'}))
    biography = forms.CharField(label="", max_length=160, widget=forms.widgets.TextInput(attrs={':maxlength':'max_bio', 'v-model':'bio','placeholder': 'Add your bio', 'class': 'form-control', '@focus':'bio_focus = true', '@blur':'bio_focus = false'}))
    p_x = forms.FloatField(required=False, widget=forms.HiddenInput(attrs={'v-model':'profile_coordinates.left'}))
    p_y = forms.FloatField(required=False, widget=forms.HiddenInput(attrs={'v-model':'profile_coordinates.top'}))
    p_width = forms.FloatField(required=False, widget=forms.HiddenInput(attrs={'v-model':'profile_coordinates.width'}))
    p_height = forms.FloatField(required=False, widget=forms.HiddenInput(attrs={'v-model':'profile_coordinates.height'}))
    b_x = forms.FloatField(required=False, widget=forms.HiddenInput(attrs={'v-model':'banner_coordinates.left'}))
    b_y = forms.FloatField(required=False, widget=forms.HiddenInput(attrs={'v-model':'banner_coordinates.top'}))
    b_width = forms.FloatField(required=False, widget=forms.HiddenInput(attrs={'v-model':'banner_coordinates.width'}))
    b_height = forms.FloatField(required=False, widget=forms.HiddenInput(attrs={'v-model':'banner_coordinates.height'}))

    class Meta:
        model = TwitterProfile
        fields = ('banner_picture', 'profile_picture', 'username', 'biography', 'p_x', 'p_y', 'p_width', 'p_height', 'b_x', 'b_y', 'b_width', 'b_height')



class SignupForm(UserCreationForm):
    user_regex = RegexValidator(regex=r'^[a-zA-Z0-9_]+$', message="Username must only contain only alphanumerical characters and underscores. ABC, abc, 123, _")
    email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    username = forms.CharField(validators=[user_regex], max_length=15, widget=forms.widgets.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    name = forms.CharField(max_length=50, widget=forms.widgets.TextInput(attrs={'placeholder': 'Screen name', 'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password Confirmation', 'class': 'form-control'}))

    class Meta:
        fields = ['email', 'username', 'name', 'first_name', 'last_name', 'password1', 'password2']
        model = User

class SigninForm(AuthenticationForm):
  username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
  password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))

class ChangeUsernameForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.widgets.TextInput(attrs={'v-model':'message','placeholder': 'Choose a username', 'class': 'form-control'}))

    class Meta:
        fields = ['username']
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username) #this raises an ObjectDoesNotExist exception if it doesn't find a user with that username
        except ObjectDoesNotExist:
            return username #if username doesn't exist
        raise forms.ValidationError('Username is already taken.')

class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label="New Password", widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    password2 = forms.CharField(label="New Password Confirmation", widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password Confirmation', 'class': 'form-control'}))

    class Meta:
        fields = ['password1', 'password2']

class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.widgets.TextInput(attrs={'v-model':'message','placeholder': 'Choose an email', 'class': 'form-control'}))

    class Meta:
        fields = ['email']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email) #this raises an ObjectDoesNotExist exception if it doesn't find a user with that email
        except ObjectDoesNotExist:
            return email #if email doesn't exist
        raise forms.ValidationError('Email is already being used.')

class ChangePhoneForm(forms.Form):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$', message="Phone number must be entered in the format: '(999) 999-9999'. Up to 10 digits allowed.")
    phone_number = forms.CharField(validators=[phone_regex], label="Phone Number", widget=forms.widgets.TextInput(attrs={'v-model':'message','placeholder': '(xxx) xxx-xxxx', 'class': 'form-control'}))

    class Meta:
        fields = ['phone_number']

 