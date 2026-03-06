from django import forms
from recipes.models import Recipe

class AddRecipeForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('MAIN', 'Delicious Main Course'),
        ('START', 'Quick Starter'),
        ('DESSERT', 'Sweet Treats'),
    ]
    title = forms.CharField(max_length=50,
                            help_text= "Enter the title of the recipe.")
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}), 
        help_text="Describe the ingredients and steps."
    )
    image = forms.ImageField()
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

    class Meta:
        model = Recipe
        fields = ('title','description','image','category')