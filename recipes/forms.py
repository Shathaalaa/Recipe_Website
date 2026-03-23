from django import forms
from django.contrib.auth.models import User
from recipes.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
from recipes.models import Recipe

class AddRecipeForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('Vegetarian', 'Vegetarian'),
        ('Asian', 'Asian'),
        ('Middle Eastern', 'Middle Eastern'),
        ('American', 'American'),
        ('Side Dishes', 'Side Dishes'),
        ('Drinks', 'Drinks'),
        ('Desserts', 'Desserts'),
        ('Italian', 'Italian'),
    ]

    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'image', 'category',
            'prep_time', 'cook_time', 'servings', 'ingredients', 'steps'
        ]
        
