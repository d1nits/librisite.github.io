from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class ForumThread(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        base_slug = self.slug
        counter = 1
        while ForumThread.objects.filter(slug=self.slug).exists():
            self.slug = f"{base_slug}-{counter}"
            counter += 1

        super().save(*args, **kwargs)


class Comment(models.Model):
        thread = models.ForeignKey(ForumThread, related_name='comments', on_delete=models.CASCADE)
        author = models.ForeignKey(User, on_delete=models.CASCADE)
        content = models.TextField()
        parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
        
        def __str__(self):
             return self.content



