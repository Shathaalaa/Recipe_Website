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
            "image": 'recipe_photos/spicy_pasta.jpeg',
            "category": "Italian",
            "prep_time": 10,
            "cook_time": 30,
            "servings": 2,
            "ingredients": "2 garlic cloves, 2 tbsp olive oil, 1 red chilli, 1 400g tin of chopped tomatoes",
            "steps": """Pour the oil into a saucepan and fry the garlic over a medium heat for 1-2 mins until fragrant, but not browned. 
            Add the chilli, fry for another minute, then add the tomatoes along with 1 tsp salt and ½ tsp sugar. 
            Stir well to combine the ingredients and simmer gently for 20 mins, stirring regularly. The sauce will thicken slowly as it cooks.
            Taste and adjust the seasoning if needed. Serve stirred through pasta, or blend it first to create a smoother sauce if you prefer. 
            Will keep chilled for up to five days."""
        },
        {
            "title": "Classic Caesar Salad",
            "description": "Crisp romaine lettuce and croutons dressed with lemon juice, olive oil, egg, Worcestershire sauce, anchovies, and garlic.",
            "image": 'recipe_photos/caesar-salad.jpeg',
            "category": "Side Dishes",
            "prep_time": 15,
            "cook_time": 0,
            "servings": 3,
            "ingredients": "3 tbsp olive oil, 1 large romaine lettuce, 1 medium ciabatta loaf, 1 garlic clove, 2 anchovies, parmesan, mayonnaise, white wine vinegar",
            "steps": """Heat oven to 200C/fan 180C/gas 6. Tear 1 medium ciabatta into big, ragged croutons or, if you prefer, cut with a bread knife. Spread over a large baking sheet or tray and sprinkle over 2 tbsp olive oil.
            Rub the oil into the bread and season with a little salt if you like (sea salt crystals are best for this). Bake for 8-10 mins, turning the croutons a few times during cooking so they brown evenly.
            Bash 1 garlic clove with the flat of a knife and peel off the skin. Crush with a garlic crusher. Mash 2 anchovies with a fork against the side of a small bowl.
            Grate a handful of parmesan cheese and mix with the garlic, anchovies, 5 tbsp Hellmann's Real Mayonnaise and 1 tbsp white wine vinegar. Season to taste. It should be the consistency of yogurt – if yours is thicker, stir in a few tsps water to thin it.
            Shave the cheese with a peeler. Tear 1 large cos or romaine lettuce into large pieces and put in a large bowl.
            Add most of the dressing and toss with your fingers. Scatter the rest of the chicken and croutons, then drizzle with the remaining dressing. Sprinkle the parmesan on top and serve straight away."""
        },
        {
            "title": "Chocolate Lava Cake",
            "description": "A popular dessert that combines the elements of a flourless chocolate cake and a soufflé.",
            "image": 'recipe_photos/chocolate lave.jpeg',
            "category": "Desserts",
            "prep_time": 10,
            "cook_time": 30,
            "servings": 8,
            "ingredients": "100g butter, 100g dark chocolate, 150g light brown sugar, 3 large eggs, 1/2 tsp vanilla extract, 50g plain flour",
            "steps": """Heat oven to 200C/180C fan/gas 6. Butter 6 dariole moulds or basins well and place on a baking tray. 
            Put 100g butter and 100g chopped dark chocolate in a heatproof bowl and set over a pan of hot water (or alternatively put in the microwave and melt in 30 second bursts on a low setting) and stir until smooth. Set aside to cool slightly for 15 mins.
            Using an electric hand whisk, mix in 150g light brown soft sugar, then 3 large eggs, one at a time, followed by ½ tsp vanilla extract and finally 50g plain flour. Divide the mixture among the darioles or basins.
            You can now either put the mixture in the fridge, or freezer until you're ready to bake them. Can be cooked straight from frozen for 16 mins, or bake now for 10-12 mins until the tops are firm to the touch but the middles still feel squidgy.
            Carefully run a knife around the edge of each pudding, then turn out onto serving plates and serve with single cream."""
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
                'author': user,
                'prep_time': data['prep_time'],
                'cook_time': data['cook_time'],
                'servings': data['servings'],
                'ingredients': data['ingredients'],
                'steps': data['steps']
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