# Import django forms and models

from django import forms
from django.utils.html import strip_tags

from .models import Tweet

class TweetForm(forms.ModelForm):
    body = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={'placeholder': 'What is happening?', 'class': 'form-control'}))
    tweet_id = forms.FloatField(required=False, widget=forms.HiddenInput(attrs={'v-model':'tweet_id'}))
    parent_id = forms.FloatField(required=False, widget=forms.HiddenInput(attrs={'v-model':'parent_id'}))
 
    class Meta:
        model = Tweet
        exclude = ('user','parent','likes')
        widgets = {
            'parent': forms.HiddenInput(),
        }
        fields = ('body','tweet_id','parent_id')