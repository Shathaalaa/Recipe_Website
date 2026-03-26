from django.test import TestCase
from django.db import models
import recipes.forms
from recipes.forms import AddRecipeForm
from django.conf import settings
import recipes.models
import tempfile
from recipes.models import Recipe, Like, Comment
from django.contrib.auth.models import User

class RecipeCreationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'testuser',
            email = 'test@test.com',
            password = 'testpass123',
        )
    
    def test_create_recipe_with_valid_data(self):
        recipe = AddRecipeForm({'title': 'test title', 
                             'description': 'test description',
                             'image': tempfile.NamedTemporaryFile(suffix=".jpg").name,
                             'category': 'Asian',
                             'prep_time': 5,
                             'cook_time': 10,
                             'servings': 2,
                             'ingredients': 'test ingredients',
                             'steps': 'test steps'})
        self.assertTrue(recipe.is_valid())

    def test_create_recipe_no_image(self):
        recipe = AddRecipeForm({'title': 'test title', 
                             'description': 'test description',
                             'category': 'Asian',
                             'prep_time': 5,
                             'cook_time': 10,
                             'servings': 2,
                             'ingredients': 'test ingredients',
                             'steps': 'test steps'})
        self.assertTrue(recipe.is_valid())

    def test_create_recipe_with_no_title(self):
        recipe = AddRecipeForm({'description': 'test description',
                             'image': tempfile.NamedTemporaryFile(suffix=".jpg").name,
                             'category': 'Asian',
                             'prep_time': 5,
                             'cook_time': 10,
                             'servings': 2,
                             'ingredients': 'test ingredients',
                             'steps': 'test steps'})
        self.assertFalse(recipe.is_valid())

    def test_create_recipe_assigns_date(self):
        recipe = Recipe.objects.create(title= 'test title', 
                             description= 'test description',
                             image= None,
                             category= 'Asian',
                             prep_time= 5,
                             cook_time= 10,
                             servings= 2,
                             ingredients= 'test ingredients',
                             steps= 'test steps',
                             author= self.user,)
        self.assertIsNotNone(recipe.created_at)

        from django.utils import timezone
        now = timezone.now()
        time_difference = (now - recipe.created_at).total_seconds()
        max_time_difference = 5

        self.assertLess(time_difference, max_time_difference)

    def test_recipe_likes(self):
        recipe = Recipe.objects.create(title= 'test title', 
                             description= 'test description',
                             image= None,
                             category= 'Asian',
                             prep_time= 5,
                             cook_time= 10,
                             servings= 2,
                             ingredients= 'test ingredients',
                             steps= 'test steps',
                             author= self.user,)
        
        self.assertIsNotNone(recipe.total_likes())
        
        like = Like.objects.create(user = self.user,
                                   recipe = recipe,)
        
        self.assertEqual(recipe.total_likes(), 1)

    def test_recipe_comments(self):
        recipe = Recipe.objects.create(title= 'test title', 
                             description= 'test description',
                             image= None,
                             category= 'Asian',
                             prep_time= 5,
                             cook_time= 10,
                             servings= 2,
                             ingredients= 'test ingredients',
                             steps= 'test steps',
                             author= self.user,)
        
        comment = Comment.objects.create(recipe = recipe,
                                         user = self.user,
                                         text = "Test comment")
        
        self.assertEqual(recipe.comments.count(), 1)
        print("First comment:")
        print(recipe.comments.first())
        self.assertEqual(recipe.comments.first().text, "Test comment")
        
