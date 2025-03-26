from django import forms
from .models import UserProfile

class EditProfileForm(forms.ModelForm):
    
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Tell us about yourself...'}),
        required=False  
    )  
    
    picture = forms.ImageField(required=False)  

    
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    age = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Age'}))
    meal_preferences = forms.MultipleChoiceField(
        required=False,
        choices=[
            ('Asian', 'Asian'),
            ('Latin American', 'Latin American'),
            ('Fast Food', 'Fast Food'),
        ],
        widget=forms.CheckboxSelectMultiple
    )
    budget = forms.ChoiceField(
        required=False,
        choices=[('$', 'Low'), ('$$', 'Medium'), ('$$$', 'High')],
        widget=forms.Select
    )
    age_range = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Age Range (e.g., 19-21)'}),
    )
    dietary_needs = forms.MultipleChoiceField(
        required=False,
        choices=[('Nut Allergy', 'Nut Allergy'), ('Vegetarian', 'Vegetarian')],
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = UserProfile
        fields = ['bio', 'picture', 'phone_number', 'age', 'meal_preferences', 'budget', 'age_range', 'dietary_needs']  # All fields from the form
