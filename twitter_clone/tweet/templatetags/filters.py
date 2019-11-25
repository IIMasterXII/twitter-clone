from django import template
from django.utils.html import format_html, escape
from django.utils.timesince import timesince
from datetime import *
from django.utils.timezone import utc

register = template.Library()

@register.filter(name='time_difference')
def time_difference(value):
    now = datetime.utcnow().replace(tzinfo=utc)
    try:
        difference = now - value
    except:
        return value

    if difference <= timedelta(minutes=1):
        return 'Just now'
    return '%(time)s ago' % {'time': timesince(value).split(', ')[0]}

@register.filter(name='parse_tweet_text')
def parse_tweet_text(tweet_object, autoescape=False):
    parsed_tweet_dict = tweet_object.parse_all()

    # return a dictionary that looks like
    # {'hashtag0': <span>#hash</span", 'mention0': <a>@mike</a>}
    encoded = encode_tweet(parsed_tweet_dict)

    # merge
    parsed_tweet_dict[u'parsed_text'] = escape(
        parsed_tweet_dict[u'parsed_text'])
    statement = parsed_tweet_dict.get(u'parsed_text').format(**encoded)
    return statement


def encode_tweet(parsed_tweet_dict):
    result = {}

    # adding html component to hashtags
    for index, value in enumerate(parsed_tweet_dict.get(u'hashtags')):
        result['hashtag'+str(index)] = \
            u'<span class="hashtag position-relative"><a href="{link}">#{hashtag}</a></span>'\
                .format(hashtag=escape(value), link="/hashtag/{0}"\
                .format(escape(value)))

    # adding html component to mentions
    for index, value in enumerate(parsed_tweet_dict.get(u'mentions')):
        result['mention'+str(index)] = \
            u'<span class="mention position-relative"><a href="{link}">@{mention}</a></span>'\
                .format(mention=escape(value), link="/{0}"\
                .format(escape(value)))

    return result

@register.inclusion_tag('tweet.html')
def get_tweets(tweets, user, form, isStatus=False):
    return {'tweets': tweets, 'user':user, 'form':form, 'status':isStatus}

@register.filter(name='merge')
def merge_tweets(tweet, replies):
    merged_tweets = tweet | replies
    return merged_tweets