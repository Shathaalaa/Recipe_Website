from django.test import TestCase, Client
from django.contrib.auth.models import User
from recipes.models import Recipe, Like
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


class RecipeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="testpass123"
        )

        self.recipe = Recipe.objects.create(
            title="Pasta",
            description="Simple pasta recipe",
            category="Italian",
            author=self.user,
            prep_time=10,
            cook_time=20,
            servings=2,
            ingredients="pasta,tomato,cheese",
            steps="Boil pasta.Add sauce.Serve."
        )

    def test_recipe_str_returns_title(self):
        self.assertEqual(str(self.recipe), "Pasta")

    def test_total_time_property(self):
        self.assertEqual(self.recipe.total_time, 30)

    def test_total_likes_initially_zero(self):
        self.assertEqual(self.recipe.total_likes(), 0)

    def test_total_likes_after_like_created(self):
        Like.objects.create(user=self.user, recipe=self.recipe)
        self.assertEqual(self.recipe.total_likes(), 1)


class RecipeViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username="viewer",
            email="viewer@example.com",
            password="testpass123"
        )

        self.test_image = SimpleUploadedFile(
            name="test.jpg",
            content=b"file_content",
            content_type="image/jpeg"
        )

        self.recipe = Recipe.objects.create(
            title="Burger",
            description="Nice burger",
            image=self.test_image,
            category="American",
            author=self.user,
            prep_time=15,
            cook_time=10,
            servings=1,
            ingredients="bun,beef,lettuce",
            steps="Cook beef.Assemble burger.Serve."
        )

    def test_recipe_list_page_status_code(self):
        response = self.client.get(reverse("recipes:recipe_list"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_list_uses_correct_template(self):
        response = self.client.get(reverse("recipes:recipe_list"))
        self.assertTemplateUsed(response, "recipes/recipe_list.html")

    def test_recipe_list_contains_recipe_title(self):
        response = self.client.get(reverse("recipes:recipe_list"))
        self.assertContains(response, "Burger")

    def test_recipe_detail_page_status_code(self):
        response = self.client.get(
            reverse("recipes:recipe_detail", args=[self.recipe.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_contains_description(self):
        response = self.client.get(
            reverse("recipes:recipe_detail", args=[self.recipe.id])
        )
        self.assertContains(response, "Nice burger")

    def test_recipe_by_category_filters_results(self):
        response = self.client.get(
            reverse("recipes:recipe_by_category", args=["American"])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Burger")


class RecipeAuthTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username="authuser",
            email="authuser@example.com",
            password="testpass123"
        )

        self.recipe = Recipe.objects.create(
            title="Salad",
            description="Healthy salad",
            category="Vegetarian",
            author=self.user,
            prep_time=5,
            cook_time=0,
            servings=2,
            ingredients="lettuce,tomato,cucumber",
            steps="Wash ingredients.Mix together.Serve."
        )

    def test_add_recipe_requires_login(self):
        response = self.client.get(reverse("recipes:add_recipe"))
        self.assertEqual(response.status_code, 302)

    def test_profile_requires_login(self):
        response = self.client.get(reverse("recipes:profile_default"))
        self.assertEqual(response.status_code, 302)


class RecipeInteractionTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username="liker",
            email="liker@example.com",
            password="testpass123"
        )

        self.recipe = Recipe.objects.create(
            title="Soup",
            description="Warm soup",
            category="Side Dishes",
            author=self.user,
            prep_time=10,
            cook_time=30,
            servings=3,
            ingredients="water,vegetables,salt",
            steps="Boil water.Add vegetables.Serve."
        )

    def test_like_ajax_requires_login(self):
        response = self.client.post(
            reverse("recipes:like_recipe_ajax", args=[self.recipe.id])
        )
        self.assertEqual(response.status_code, 401)

    def test_logged_in_user_can_like_recipe(self):
        self.client.login(username="liker", password="testpass123")

        response = self.client.post(
            reverse("recipes:like_recipe_ajax", args=[self.recipe.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.count(), 1)

    def test_logged_in_user_can_unlike_recipe(self):
        Like.objects.create(user=self.user, recipe=self.recipe)
        self.client.login(username="liker", password="testpass123")

        response = self.client.post(
            reverse("recipes:like_recipe_ajax", args=[self.recipe.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.count(), 0)


class RecipeCommentTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username="commenter",
            email="commenter@example.com",
            password="testpass123"
        )

        self.recipe = Recipe.objects.create(
            title="Pizza",
            description="Cheesy pizza",
            category="Italian",
            author=self.user,
            prep_time=15,
            cook_time=20,
            servings=2,
            ingredients="dough,cheese,tomato sauce",
            steps="Prepare dough.Add toppings.Bake."
        )

    def test_add_comment_requires_login(self):
        response = self.client.post(
            reverse("recipes:add_comment", args=[self.recipe.id]),
            {"text": "Looks great!"}
        )
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_add_comment(self):
        self.client.login(username="commenter", password="testpass123")

        response = self.client.post(
            reverse("recipes:add_comment", args=[self.recipe.id]),
            {"text": "Looks great!"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.recipe.comments.count(), 1)
        self.assertEqual(self.recipe.comments.first().text, "Looks great!")


class RecipeProfileTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username="profileuser",
            email="profileuser@example.com",
            password="testpass123"
        )

        self.test_image = SimpleUploadedFile(
            name="profile_test.jpg",
            content=b"file_content",
            content_type="image/jpeg"
        )

        self.recipe = Recipe.objects.create(
            title="Profile Recipe",
            description="Recipe shown on profile page",
            image=self.test_image,
            category="Italian",
            author=self.user,
            prep_time=10,
            cook_time=15,
            servings=2,
            ingredients="pasta,tomato,cheese",
            steps="Cook pasta.Add sauce.Serve."
        )

    def test_logged_in_user_can_open_profile_page(self):
        self.client.login(username="profileuser", password="testpass123")

        response = self.client.get(reverse("recipes:profile_default"))

        self.assertEqual(response.status_code, 200)

    def test_profile_page_uses_correct_template(self):
        self.client.login(username="profileuser", password="testpass123")

        response = self.client.get(reverse("recipes:profile_default"))

        self.assertTemplateUsed(response, "recipes/profile.html")

    def test_profile_page_contains_user_recipe(self):
        self.client.login(username="profileuser", password="testpass123")

        response = self.client.get(reverse("recipes:profile_default"))

        self.assertContains(response, "Profile Recipe")