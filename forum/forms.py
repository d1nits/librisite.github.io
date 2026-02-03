from django import forms
from .models import Comment, ForumThread
from django.contrib.contenttypes.models import ContentType


class ForumThreadForm(forms.ModelForm):
    class Meta:
        model = ForumThread
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


    
    