from django import forms
from .models import UserProfile

from django import forms
from .models import UserProfile

class EditProfileForm(forms.ModelForm):
    bio = forms.CharField(
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
    
    cuisines = forms.ChoiceField(
        required=False,
        choices=[
            ('Asian', 'Asian'),
            ('Italian', 'Italian'),
            ('Mediterranean', 'Mediterranean'),
            ('Indian', 'Indian'),
            ('Latin American', 'Latin American'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    dining_vibes = forms.ChoiceField(
        required=False,
        choices=[
            ('Fast Food', 'Fast Food'),
            ('Fine Dining', 'Fine Dining'),
            ('Healthy & Organic', 'Healthy & Organic'),
            ('Brunch & Breakfast', 'Brunch & Breakfast'),
            ('Café & Coffee', 'Café & Coffee'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    budget = forms.ChoiceField(
        required=True,
        choices=[
            ('$', 'Low'),
            ('$$', 'Medium'),
            ('$$$', 'High'),
            ('$$$$', 'Luxury'),
        ],
        initial='$',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    age_range = forms.ChoiceField(
        required=False,
        choices=[
            ('16-19', '16-19'),
            ('19-21', '19-21'),
            ('21-23', '21-23'),
            ('24-26', '24-26'),
            ('27+', '27+'),
        ],
        initial='19-21',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    dietary_needs = forms.ChoiceField(
        required=False,
        choices=[
            ('Vegetarian', 'Vegetarian'),
            ('Vegan', 'Vegan'),
            ('Keto', 'Keto / Low-carb'),
            ('Gluten-free', 'Gluten-free'),
            ('Nut Allergy', 'Nut Allergy'),
            ('Lactose Intolerant', 'Lactose Intolerant'),
            ('Pescatarian', 'Pescatarian'),
            ('No Restrictions', 'No Restrictions'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = ['bio', 'picture', 'phone_number', 'age', 'cuisines', 'dining_vibes', 
                 'budget', 'age_range', 'dietary_needs']


class UserPreferencesForm(forms.ModelForm):
    
    cuisines = forms.ChoiceField(
        required=True,
        choices=[
            ('Asian', 'Asian'),
            ('Italian', 'Italian'),
            ('Mediterranean', 'Mediterranean'),
            ('Indian', 'Indian'),
            ('Latin American', 'Latin American'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    dining_vibes = forms.ChoiceField(
        required=True,
        choices=[
            ('Fast Food', 'Fast Food'),
            ('Fine Dining', 'Fine Dining'),
            ('Healthy & Organic', 'Healthy & Organic'),
            ('Brunch & Breakfast', 'Brunch & Breakfast'),
            ('Café & Coffee', 'Café & Coffee'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    budget = forms.ChoiceField(
        required=True,
        choices=[
            ('$', 'Low'),
            ('$$', 'Medium'),
            ('$$$', 'High'),
            ('$$$$', 'Luxury'),
        ],
        initial='$',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    age_range = forms.ChoiceField(
        required=True,
        choices=[
            ('16-19', '16-19'),
            ('19-21', '19-21'),
            ('21-23', '21-23'),
            ('24-26', '24-26'),
            ('27+', '27+'),
        ],
        initial='19-21',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    dietary_needs = forms.ChoiceField(
        required=True,
        choices=[
            ('Vegetarian', 'Vegetarian'),
            ('Vegan', 'Vegan'),
            ('Keto', 'Keto / Low-carb'),
            ('Gluten-free', 'Gluten-free'),
            ('Nut Allergy', 'Nut Allergy'),
            ('Lactose Intolerant', 'Lactose Intolerant'),
            ('Pescatarian', 'Pescatarian'),
            ('No Restrictions', 'No Restrictions'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = ['cuisines', 'dining_vibes', 'budget', 'age_range', 'dietary_needs']

