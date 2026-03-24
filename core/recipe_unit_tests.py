from django.test import TestCase
from django.db import models
import recipes.forms
from recipes.forms import AddRecipeForm
from django.conf import settings
import recipes.models

class RecipeCreationTest(TestCase):
    def test_create_recipe_with_valid_data(self):
        form = AddRecipeForm()
        self.assertTrue(form.is_valid())