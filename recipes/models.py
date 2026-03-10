from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    # The additional attributes we wish to include.
    picture = models.ImageField(default= 'default.jpg',upload_to='profile_images',blank=True)

    def __str__(self):
        return self.user.username