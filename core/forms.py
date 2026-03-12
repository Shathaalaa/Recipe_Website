from django import forms 


class ContactForm(forms.Form):
    name = forms.CharField(max_length=128, help_text="Name")
    email = forms.EmailField(max_length=256, help_text="Email")
    message = forms.CharField(max_length=2048, help_text="Message", widget=forms.Textarea)

