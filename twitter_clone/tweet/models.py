import uuid
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from twitter_profile.models import TwitterProfile

class Tweet(models.Model):
    user        = models.ForeignKey(User, related_name='tweets', on_delete=models.DO_NOTHING)
    parent      = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.DO_NOTHING)
    body        = models.CharField(max_length=255)
    likes       = models.ManyToManyField(TwitterProfile, blank=True, related_name='post_likes')
    created_at  = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    @property
    def total_likes(self):
        return self.likes.count()
 
    def parse_hashtags(self):
        return [slugify(i) for i in self.body.split() if i.startswith("#")]

    def parse_mentions(self):
        mentions = [slugify(i) for i in self.body.split() if i.startswith("@")]
        return User.objects.filter(username__in=mentions)

    def parse_all(self):
        parts = self.body.split()
        hashtag_counter = 0
        mention_counter = 0
        result = {"parsed_text": "", "hashtags": [], "mentions": []}
        for index, value in enumerate(parts):
            if value.startswith("#"):
                parts[index] = "{hashtag" + str(hashtag_counter) + "}"
                hashtag_counter += 1
                result[u'hashtags'].append(slugify(value))
            if value.startswith("@"):
                parts[index] = "{mention" + str(mention_counter) + "}"
                mention_counter += 1
                result[u'mentions'].append(slugify(value))
        result[u'parsed_text'] = " ".join(parts)
        return result
