from django.contrib import admin
from .models import ForumThread, Comment

admin.site.register(ForumThread)
admin.site.register(Comment)
