import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RecipeSite.settings')
import django
django.setup()
from recipes.models import Recipe
from django.contrib.auth.models import User

def populate():
    user, created = User.objects.get_or_create(username='admin')

    # 3. Your list of recipe data
    recipes = [
        {
            "title": "Spicy Arrabbiata Pasta",
            "description": "A delicious spicy Italian pasta dish with garlic, tomatoes, and dried red chili peppers cooked in olive oil.",
            "image": "https://example.com/pasta.jpg",
            "category": "Main Course"
        },
        {
            "title": "Classic Caesar Salad",
            "description": "Crisp romaine lettuce and croutons dressed with lemon juice, olive oil, egg, Worcestershire sauce, anchovies, and garlic.",
            "image": "https://example.com/salad.jpg",
            "category": "Starter"
        },
        {
            "title": "Chocolate Lava Cake",
            "description": "A popular dessert that combines the elements of a flourless chocolate cake and a soufflé.",
            "image": "https://example.com/cake.jpg",
            "category": "Dessert"
        },
        {
            "title": "Homemade Margherita Pizza",
            "description": "Simple pizza with San Marzano tomatoes, mozzarella cheese, fresh basil, salt, and extra-virgin olive oil.",
            "image": "https://example.com/pizza.jpg",
            "category": "Main Course"
        }
    ]

    # 4. Loop through and save to the database
    for data in recipes:
        # get_or_create prevents duplicate recipes if you run the script twice
        recipe, created = Recipe.objects.get_or_create(
            title=data['title'],
            defaults={
                'description': data['description'],
                'image': data['image'],
                'category': data['category'],
                'author': user
            }
        )
        if created:
            print(f"- Added: {recipe.title}")
        else:
            print(f"- Already exists: {recipe.title}")

if __name__ == '__main__':
    print("Starting Recipe population script...")
    populate()
    print("Done!")