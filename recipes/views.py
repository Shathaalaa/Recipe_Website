from django.shortcuts import render,redirect
from .forms import AddRecipeForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit = False)
            recipe.author = request.user
            recipe.save()
            return redirect('profile')
        else:
            print(form.errors)
    else:
        form = AddRecipeForm()
    return render(request, 'add_recipe.html', {'form':form})