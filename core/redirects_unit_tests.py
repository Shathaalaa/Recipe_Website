from django.test import TestCase, Client
from django.contrib.auth.models import User
from recipes.models import Recipe
from django.urls import reverse
from unittest import mock

class LikeWithoutLoggedIn(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'testuser',
            email = 'test@test.com',
            password = 'password1234',
        )

        self.recipe = Recipe.objects.create(title= 'test title', 
            description= 'test description',
            image= None,
            category= 'Asian',
            prep_time= 5,
            cook_time= 10,
            servings= 2,
            ingredients= 'test ingredients',
            steps= 'test steps',
            author= self.user,)
        
        self.client = Client()

    def test_like_recipe_ajax_redirect_when_logged_out(self):
        url = reverse('recipes:like_recipe_ajax', args=[self.recipe.id])

        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 401)

        

    def test_google_oauth(self):
        with mock.patch('google.oauth2.id_token.verify_oauth2_token') as mock_verify_oauth2_token:
            mock_verify_oauth2_token.return_value = {
                'username' = 'test google user',
                'email' = 'test@gmail.com',
            }
            