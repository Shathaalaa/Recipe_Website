from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from recipes.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import AddRecipeForm #delete maybe
from .models import Recipe, Comment, Like
from django.http import JsonResponse
# Create your views here.

def signup(request):
    # A boolean value for telling the template
    # whether the registeration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            #Now we hash the password with the set_password
            #Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since ewe need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance
            profile.save()

            #Update our variable to indicate that the template
            #registration was successful.
            registered = True

        else:
            # Invalid form or forms - mistakes or something else?
            # print problems to the terminal.
            print(user_form.errors,profile_form.errors)

    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    # Render the template depending on the context.
    return render(request, 'recipes/signup.html',context={'user_form':user_form, 
    'profile_form':profile_form,
    'registered':registered})


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'] because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username,password=password)

        #If we have a User object, the details are correct.
        #If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage/
                login(request,user)
                return redirect('index')
            else:
                # An inactive account was used - no  loggin in!
                messages.error(request, "you're account is disabled")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            messages.error(request, "*Invalid username or password")
    
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request,'recipes/login.html')
    return render(request, 'recipes/login.html')
    

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('recipes:index'))
    
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
