from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from recipes.forms import UserForm, UserProfileForm
from django.contrib.auth.models import User
from recipes.models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
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
                return redirect(reverse('recipes:index'))
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


class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website':user_profile.website,
                                'picture':user_profile.picture})
        return (user,user_profile,form)
    
    @method_decorator(login_required)
    def get(self,request,username):
        try:
            (user,user_profile,form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('recipes:index'))
        context_dict = {'user_profile':user_profile,
                        'selected_user':user,
                        'form':form}
        return render(request,'recipes/profile.html',context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user,user_profile,form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('recipes:index'))
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect('recipes:profile',user.username)
        else:
            print(form.errors)

        context_dict = {'user_profile':user_profile,
                        'selected_user':user,
                        'form':form}
        
        return render(request, 'recipes/profile.html',context_dict)
    







