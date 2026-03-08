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
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    image = forms.ImageField()
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}), 
        help_text="Describe the recipe."
    )
    prep_time = forms.IntegerField()
    cook_time = forms.IntegerField()
    total_time = forms.IntegerField()
    serving_time = forms.IntegerField()
    ingredients = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}), 
        help_text="What ingredients are used"
    )
    steps = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}), 
        help_text="Describe the steps."
    )
    
    class Meta:
        model = Recipe
        fields = ('title','description','image','category')