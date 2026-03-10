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


# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='recipe_photos/', blank= True, null= True)
    category = models.CharField(max_length=50, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    servings = models.IntegerField()
    ingredients = models.TextField()
    steps = models.TextField()

    def total_likes(self):
        return self.like_set.count() 
    
    @property
    def total_time(self):
        return self.prep_time + self.cook_time

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Recipe Entry"
        verbose_name_plural = "All Recipes"

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.recipe.title}'
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')
