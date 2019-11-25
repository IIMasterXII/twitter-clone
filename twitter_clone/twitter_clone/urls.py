from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from twitter_profile.views import frontpage, signout, profile, profile_tabs, profile_settings, settings_tabs
from tweet.views import follows, followers, follow, stopfollow, status, feed, like, reply


urlpatterns = [
  path('', frontpage, name='frontpage'),
  path('feed/', feed, name='feed'),
  path('signout/', signout, name='signout'),
  path('admin/', admin.site.urls),
  path('settings/', profile_settings, name='profile_settings'),
  path('settings/<str:tab>', settings_tabs, name='settings_tabs'),
  path('reply/', reply, name='reply'),
  path('reply/<int:user>/<int:tweet>', reply, name='reply'),
  path('<str:username>/follows/', follows, name='follows'),
  path('<str:username>/followers/', followers, name='followers'),
  path('<str:username>/follow/', follow, name='follow'),
  path('<str:username>/stopfollow/', stopfollow, name='stopfollow'),
  path('<str:username>/status/<int:id>/', status, name='status'),
  path('<str:username>/status/<int:id>/like', like, name='like'),
  path('<str:username>/', profile, name='profile'),
  path('<str:username>/<str:tab>', profile_tabs, name='profile_tabs'),

]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)