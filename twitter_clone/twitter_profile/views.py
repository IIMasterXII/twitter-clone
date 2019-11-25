# Import django and models

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from twitter_profile.forms import SignupForm, SigninForm, ChangeUsernameForm, ChangeEmailForm, ChangePhoneForm, ChangePasswordForm, PersonalInfoForm
from tweet.forms import TweetForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from tweet.models import Tweet

# Views

@login_required
def profile(request, username):
  if request.user.is_authenticated:
    user = User.objects.get(username=username)
    
    if request.method == 'POST':
      if 'tweetform' in request.POST:
        form = TweetForm(data=request.POST)
        infoform = PersonalInfoForm()

        if form.is_valid():
          tweet = form.save(commit=False)
          tweet.user = request.user
          tweet.save()
          
          redirecturl = request.POST.get('redirect', '/')

          return redirect(redirecturl)

      else:
        infoform = PersonalInfoForm(request.POST, request.FILES)
        form = TweetForm()
        if infoform.is_valid():
          profile = request.user.twitterprofile
          if infoform.cleaned_data.get('profile_picture'):
            photo = infoform.cleaned_data.get('profile_picture')
            x = infoform.cleaned_data.get('p_x')
            y = infoform.cleaned_data.get('p_y')
            w = infoform.cleaned_data.get('p_width')
            h = infoform.cleaned_data.get('p_height')
            profile.crop_profile_picture(photo,x,y,w,h)
          if infoform.cleaned_data.get('banner_picture'):
            photo = infoform.cleaned_data.get('banner_picture')
            x = infoform.cleaned_data.get('b_x')
            y = infoform.cleaned_data.get('b_y')
            w = infoform.cleaned_data.get('b_width')
            h = infoform.cleaned_data.get('b_height')
            profile.crop_banner_picture(photo,x,y,w,h)
          profile.username = infoform.cleaned_data.get('username')
          profile.biography = infoform.cleaned_data.get('biography')
          profile.save()
          
          redirecturl = request.POST.get('redirect', '/')

          return redirect(redirecturl)

    else:
      form = TweetForm()
      infoform = PersonalInfoForm()

    return render(request, 'profile.html', {'form': form, 'infoform': infoform, 'user': user})
  else:
    return redirect('/')

@login_required
def profile_tabs(request, username, tab):
  if request.user.is_authenticated:
    user = User.objects.get(username=username)
    liked = Tweet.objects.all().filter(likes=user.twitterprofile)
    form = TweetForm()
    infoform = PersonalInfoForm()
    return render(request, 'profile.html', {'form': form, 'infoform': infoform, 'user': user, 'liked': liked, 'tab': tab})
  else:
    return redirect('/')


@login_required
def profile_settings(request):
  if request.user.is_authenticated:
    return render(request, 'settings.html', {'user': request.user})
  else:
    return redirect('/')

@login_required
def settings_tabs(request, tab):
    if request.user.is_authenticated:

        form = None

        #screen name change
        if tab == 'screen_name':
            if request.method == 'POST':
                form = ChangeUsernameForm(request.POST or None)
                if form.is_valid():
                    if form.clean_username():
                        profile = request.user.twitterprofile
                        profile.username = form.cleaned_data['username']
                        profile.save()
            else:
                form = ChangeUsernameForm()

        #phone number change
        elif tab == 'phone':
            if request.method == 'POST':
                form = ChangePhoneForm(request.POST or None)
                if form.is_valid():
                    profile = request.user.twitterprofile
                    profile.phone_number = form.cleaned_data['phone_number']
                    profile.save()
            else:
                form = ChangePhoneForm()

        #email change
        elif tab == 'email':
            if request.method == 'POST':
                form = ChangeEmailForm(request.POST or None)
                if form.is_valid():
                    if form.clean_email():
                        request.user.email = form.cleaned_data['email']
                        request.user.save()
            else:
                form = ChangeEmailForm()

        #password change
        if tab == 'password':
            if request.method == 'POST':
                form = ChangePasswordForm(request.POST or None)
                if form.is_valid():
                    request.user.password = form.cleaned_data['password1']
                    request.user.save()
            else:
                form = ChangePasswordForm()

        #privacy change
        if tab == 'deactivateprivacy':
            profile = request.user.twitterprofile
            profile.private = False
            profile.save()
            return redirect('/settings/privacy')
        
        if tab == 'activateprivacy':
            profile = request.user.twitterprofile
            profile.private = True
            profile.save()
            return redirect('/settings/privacy')

        
        return render(request, 'settings_tabs.html', {'tab': tab, 'form': form, 'user': request.user})
    else:
        return redirect('/')

def frontpage(request):
  if request.user.is_authenticated:
    return redirect('/' + request.user.username + '/') # Change this line
  else:
    if request.method == 'POST':
      if 'signupform' in request.POST:
        signupform = SignupForm(data=request.POST)
        signinform = SigninForm()
        
        if signupform.is_valid():
          username = signupform.cleaned_data['username']
          password = signupform.cleaned_data['password1']
          signupform.save()
          user = authenticate(username=username, password=password)
          profile = user.twitterprofile
          profile.username = signupform.cleaned_data['name']
          profile.save()
          login(request, user)
          return redirect('/')
      else:
        signinform = SigninForm(data=request.POST)
        signupform = SignupForm()
        
        if signinform.is_valid():
          login(request, signinform.get_user())
          return redirect('/')
    else:
        signupform = SignupForm()
        signinform = SigninForm()
  
    return render(request, 'frontpage.html', {'signupform': signupform, 'signinform': signinform})

@login_required
def signout(request):
  logout(request)
  return redirect('/')
