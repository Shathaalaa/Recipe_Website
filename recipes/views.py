from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import AddRecipeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Recipe, Comment, Like
from django.http import JsonResponse

def recipe_list(request, category=None):
    if category:
        recipes = Recipe.objects.filter(category__iexact=category)
    else:
        recipes = Recipe.objects.all()

    categories = [ "Vegetarian", "Asian", "Middle Eastern", "American", "Side dishes", "Drinks", "Desserts", "Italian"]

    return render(request, "recipes/recipe_list.html", {
        "recipes": recipes,
        "categories": categories,
        "selected_category": category
    })

def recipe_by_category(request, category_name):

    recipes = Recipe.objects.filter(category__iexact=category_name)

    categories = Recipe.objects.values_list('category', flat=True).distinct()

    context = {
        'recipes': recipes,
        'categories': categories,
        'selected_category': category_name
    }

    return render(request, 'recipes/recipe_list.html', context)

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients_list = recipe.ingredients.split(',')
    recipe_steps = recipe.steps.split('.')[:-1]
    comments = recipe.comments.all().order_by('-created_at')
    liked = False
    if request.user.is_authenticated:
        liked = recipe.like_set.filter(user=request.user).exists()

    context = {
        'recipe': recipe,
        'ingredients_list': ingredients_list,
        'recipe_steps': recipe_steps,
        'comments': comments,
        'liked': liked
    }

    return render(request, 'recipes/recipe_detail.html', context)

@login_required
def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('recipes:recipe_list')
        else:
            print(form.errors)
    else:
        form = AddRecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})

@login_required
def add_comment(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        text = request.POST.get('text')
        if text:
            Comment.objects.create(recipe=recipe, user=request.user, text=text)
    return redirect('recipes:recipe_detail', recipe_id=recipe_id)

@login_required
def like_recipe_ajax(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = request.user

    like = Like.objects.filter(user=user, recipe=recipe).first()
    if like:
        like.delete()
        liked = False
    else:
        Like.objects.create(user=user, recipe=recipe)
        liked = True

    data = {
        'liked': liked,
        'total_likes': recipe.like_set.count()
    }
    return JsonResponse(data)