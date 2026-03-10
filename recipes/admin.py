from django.contrib import admin
from recipes.models import UserProfile

# Register your models here.
admin.site.register(UserProfile)
from .models import Recipe

# Register your models here.
admin.site.register(Recipe)
