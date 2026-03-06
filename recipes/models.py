from django.db import models
from django.contrib.auth.models import User


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
    total_time = models.IntegerField()
    serving = models.IntegerField()
    ingredients = models.TextField()
    steps = models.TextField()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Recipe Entry"
        verbose_name_plural = "All Recipes"
