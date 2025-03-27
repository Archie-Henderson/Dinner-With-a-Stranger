from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
#from django_multiselectfield import MultiSelectField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    description = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=20, unique=True)
    age = models.IntegerField(validators=[MinValueValidator(16), MaxValueValidator(100)])
    max_age_difference = models.PositiveIntegerField(validators=[MaxValueValidator(20)])

    cuisines = models.CharField(max_length=20,blank=True)

    dining_vibes = models.CharField(max_length=20, blank=True)

    
    budget = models.CharField(max_length=5, default='$')

    age_range = models.CharField(max_length=10, default='19-21')


    dietary_needs = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username
