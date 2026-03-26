from django.contrib.auth.models import User
from recipes.models import Recipe, Like, UserProfile
from django.test import TestCase
from recipes.forms import AddRecipeForm
import tempfile



class UserProfileTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username = 'testuser1',
            email = 'test1@test.com',
            password = 'testpass1234',
        )

        self.user2 = User.objects.create_user(
            username = 'testuser2',
            email = 'test2@test.com',
            password = 'testpass1234',
        )

        #self.profile1 = UserProfile.objects.create(user=self.user1)
        #self.profile2 = UserProfile.objects.create(user=self.user2)

    def test_created_recipe_in_profile(self):
        recipe = AddRecipeForm({'title': 'test title', 
            'description': 'test description',
            'image': tempfile.NamedTemporaryFile(suffix=".jpg").name,
            'category': 'Asian',
            'prep_time': 5,
            'cook_time': 10,
            'servings': 2,
            'ingredients': 'test ingredients',
            'steps': 'test steps'})
        
        