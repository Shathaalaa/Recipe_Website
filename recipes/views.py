from django.shortcuts import render

recipes_data = [
    {
        "id": 1,
        "title": "Shakshuka",
        "image": "https://images.unsplash.com/photo-1598514983318-2f64f8f4796c",
        "category": "Middle Eastern",
        "username": "Shatha",
        "description": "A flavorful Middle Eastern dish of poached eggs simmered in a spiced tomato and pepper sauce, often served with warm bread for dipping."
    },
    {
        "id": 2,
        "title": "Fruit Bowl",
        "image": "https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea",
        "category": "Vegetarian",
        "username": "Sara",
        "description": "A refreshing mix of crisp vegetables, olives, feta cheese, and a light olive oil dressing, inspired by the bright flavors of the Mediterranean."
    },
    {
        "id": 3,
        "title": "Chicken Skewers",
        "image": "https://images.unsplash.com/photo-1608756687911-aa1599ab3bd9",
        "category": "Asian",
        "username": "Ali",
        "description": "Golden and crunchy fried chicken with a juicy and tender inside, seasoned with a blend of herbs and spices."
    },
]

def recipe_list(request, category=None):

    recipes = recipes_data

    if category:
        recipes = [r for r in recipes if r["category"].lower() == category.lower()]

    categories = [ "Vegetarian", "Asian", "Middle Eastern", "American", "Side dishes", "Drinks", "Deserts", "Italian"]

    return render(request, "recipes/recipe_list.html", {
        "recipes": recipes,
        "categories": categories,
        "selected_category": category
    })

def recipe_by_category(request, category_name):
    recipes = Recipe.objects.filter(category=category_name)
    categories = Recipe.objects.values_list('category', flat=True).distinct()
    context = {
        'recipes': recipes,
        'categories': categories,
        'selected_category': category_name
    }
    return render(request, 'recipes/recipe_list.html', context)

def recipe_detail(request, recipe_id):
    recipes = [
        {'id': 1, 'title': 'Spaghetti Carbonara', 'description': 'Classic Italian', 'ingredients': 'Spaghetti,Eggs,Cheese,Pancetta', 'instructions': 'Boil pasta...'},
    ]
    recipe = next((r for r in recipes if r['id'] == recipe_id), None)
    if recipe:
        recipe['ingredients_list'] = recipe['ingredients'].split(',')
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})
