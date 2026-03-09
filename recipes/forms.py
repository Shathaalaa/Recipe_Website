from django import forms
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
        