from django.shortcuts import redirect, render
from .forms import ContactForm
from django.core.mail import send_mail

def index(request):
    response =  render(request, 'core/index.html')
    return response

def contact(request):
    form = ContactForm()
    
    def capitalise_name(input_name):
        capitalised_name = ""
        for i in input_name.split():
            capitalised_name += i.capitalize() + " "
        return capitalised_name.strip()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = capitalise_name(form.cleaned_data['name'])
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            print(message)


            try:
                send_mail(
                    subject="New message",
                    message="You have received a new message from " + name + " (" + email + "):\n" + message,
                    from_email="recipewebwad@gmail.com",
                    recipient_list=["recipewebwad@gmail.com"],
                    fail_silently=False,
                )
                print("Message received")
            except:
                raise Exception("Failed, try again later.")
            else:
                send_mail(
                    subject="Message received",
                    message="Hi, "+ name +", \nThank you for your message, we will get back to you shortly. \nYour message: \n"+ message,
                    from_email="recipewebwad@gmail.com",
                    recipient_list=[email],
                    fail_silently=False,
                )
                print(email)
                print("Message received confirmed")
                return redirect('core:contact')

        else:
            print(form.errors)
    return render(request, 'core/contact.html', {'form': form})

def about(request):
    return render(request, 'core/about.html')
        
