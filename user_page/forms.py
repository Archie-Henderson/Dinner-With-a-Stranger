from django import forms
from .models import UserProfile, Cuisine, DiningVibe, DietaryNeed, Budget, AgeRange

class EditProfileForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Tell us about yourself...'}),
        required=False  
    )  

    picture = forms.ImageField(required=False)  

    phone_number = forms.CharField(
        max_length=15, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'})
    )

    age = forms.IntegerField(
        required=False, 
        widget=forms.NumberInput(attrs={'placeholder': 'Age'})
    )

    regional_cuisines = forms.ModelMultipleChoiceField(
        queryset=Cuisine.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    dining_vibes = forms.ModelMultipleChoiceField(
        queryset=DiningVibe.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    budgets = forms.ModelMultipleChoiceField(
        queryset=Budget.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    age_ranges = forms.ModelMultipleChoiceField(
        queryset=AgeRange.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    dietary_needs = forms.ModelMultipleChoiceField(
        queryset=DietaryNeed.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = UserProfile
        fields = [
            'description', 'picture', 'phone_number', 'age',
            'regional_cuisines', 'dining_vibes',
            'budgets', 'age_ranges', 'dietary_needs'
        ]
