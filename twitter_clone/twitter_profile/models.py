from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import sys

class TwitterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    username = models.CharField(max_length=50, blank=True)
    biography = models.CharField(max_length=160, blank=True)
    profile_picture = models.ImageField(upload_to='profile/', blank=True)
    profile_banner = models.ImageField(upload_to='profile/', blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    private = models.BooleanField(default=False)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)

    def crop_profile_picture(self,photo,x,y,w,h):
        image = Image.open(photo)
        output = BytesIO()
        image = image.crop((x, y, w+x, h+y))
        image = image.resize((400, 400), Image.ANTIALIAS)
        image = image.convert('RGB')
        image.save(output,format='JPEG',quality=100)
        output.seek(0)
        self.profile_picture = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.profile_picture.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

        super(TwitterProfile,self).save()

    def crop_banner_picture(self,photo,x,y,w,h):
        image = Image.open(photo)
        output = BytesIO()
        image = image.crop((x, y, w+x, h+y))
        image = image.resize((1500, 500), Image.ANTIALIAS)
        image = image.convert('RGB')
        image.save(output,format='JPEG',quality=100)
        output.seek(0)
        self.profile_banner = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.profile_banner.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

        super(TwitterProfile,self).save()

User.twitterprofile = property(lambda u: TwitterProfile.objects.get_or_create(user=u)[0])