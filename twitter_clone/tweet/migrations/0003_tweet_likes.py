# Generated by Django 2.2.7 on 2019-11-04 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_profile', '0001_initial'),
        ('tweet', '0002_tweet_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='post_likes', to='twitter_profile.TwitterProfile'),
        ),
    ]
