from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound
try:
    from django.utils import simplejson as json
except ImportError:
    import json

from .models import Tweet
from tweet.forms import TweetForm
from tweet.templatetags.filters import time_difference

def feed(request):
  userids = []
  for user in request.user.twitterprofile.follows.all():
    userids.append(user.id)

  userids.append(request.user.id)
  tweets = Tweet.objects.filter(user_id__in=userids)[0:25]
  form = TweetForm()


  return render(request, 'feed.html', {'tweets': tweets,'form':form})

def follows(request, username):
  user = User.objects.get(username=username)
  twitterprofiles = user.twitterprofile.follows.select_related('user').all()
    
  return render(request, 'users.html', {'title': 'Follows', 'twitterprofiles': twitterprofiles})
  
def followers(request, username):
  user = User.objects.get(username=username)
  twitterprofiles = user.twitterprofile.followed_by.select_related('user').all()
    
  return render(request, 'users.html', {'title': 'Followers', 'twitterprofiles': twitterprofiles})

@login_required
def follow(request, username):
  user = User.objects.get(username=username)
  request.user.twitterprofile.follows.add(user.twitterprofile)
  
  return redirect('/' + user.username + '/')

@login_required
def stopfollow(request, username):
  user = User.objects.get(username=username)
  request.user.twitterprofile.follows.remove(user.twitterprofile)
  
  return redirect('/' + user.username + '/')

def status(request, username, id):
  if request.user.is_authenticated:
    owner = User.objects.get(username=username)
    status = Tweet.objects.filter(user_id=owner.id,id=id)
    replies = Tweet.objects.filter(parent=Tweet.objects.get(user_id=owner.id,id=id))
    tweets = (status | replies).order_by('created_at')
    form = TweetForm()
    return render(request, 'status.html', {'tweets': tweets, 'user': request.user, 'form': form})
  else:
    return redirect('/')

@login_required
def like(request, username, id):
  if request.user.is_authenticated:
    if request.method == 'POST':
      owner = User.objects.get(username=username)
      tweet = Tweet.objects.get(user_id=owner, id=id)
      if tweet.likes.filter(id=request.user.twitterprofile.id).exists():
        tweet.likes.remove(request.user.twitterprofile)
        liked = False
      else:
        tweet.likes.add(request.user.twitterprofile)
        liked = True

    ctx = {'like_count': tweet.total_likes, 'owner': owner.id, 'tweet': id, 'liked': liked}
    return HttpResponse(json.dumps(ctx), content_type='application/json')
  else:
    return redirect('/')

@login_required
def reply(request,user,tweet):
  if request.user.is_authenticated:   
    if request.method == 'POST':
        form = TweetForm(data=request.POST)

        if form.is_valid():
          parent_id = form.cleaned_data.get('parent_id')
          tweet_id = form.cleaned_data.get('tweet_id')
          parent = Tweet.objects.get(user_id=parent_id, id=tweet_id)
          tweet = form.save(commit=False)
          tweet.parent = parent
          tweet.user = request.user
          tweet.body = form.cleaned_data.get('body')
          tweet.save()
          
          # redirecturl = request.POST.get('redirect', '/')

          return redirect('/' + tweet.user.username + '/status/' + str(tweet.id))

    else:
      tweet = Tweet.objects.get(user_id=user, id=tweet)
      ctx = {
        'tweet_screenname':       tweet.user.twitterprofile.username,
        'tweet_username':         tweet.user.username,
        'tweet_profilepicture':   tweet.user.twitterprofile.profile_picture.url,
        'tweet_date':             time_difference(tweet.created_at),
        'tweet_text':             tweet.body,
        'tweet_id':               tweet.id,
        'user_id':                user
      }
      return HttpResponse(json.dumps(ctx), content_type='application/json')

  else:
    return redirect('/')
