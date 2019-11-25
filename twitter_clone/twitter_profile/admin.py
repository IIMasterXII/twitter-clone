from django.contrib import admin

# Register your models here.
from .models import TwitterProfile

admin.site.register(TwitterProfile)