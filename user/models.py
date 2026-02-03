from django.apps import apps
from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user/%Y/%m/%d', blank=True)
    about = models.TextField(blank=True, null=True)
    business_type = models.CharField(max_length=255, blank=True, null=True)

    @property
    def get_avatar(self):
        if self.photo:
            return self.photo.url
        return f'https://ui-avatars.com/api/?size=150&background=random&name={self.user.username}'

    def __str__(self):
        return f'Profile for user {self.user.username}'

    def get_wishlist(self):
        Book = apps.get_model('book', 'Book')  
        return Book.objects.filter(profile=self)