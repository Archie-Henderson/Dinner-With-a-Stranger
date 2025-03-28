from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Cuisine(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class DiningVibe(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class DietaryNeed(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Budget(models.Model):
    level = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.level

class AgeRange(models.Model):
    label = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.label

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    website = models.URLField(blank=True, null=True)
    picture = models.ImageField(upload_to='profile_images', blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, default="No bio yet :(")
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    age = models.IntegerField(validators=[MinValueValidator(16), MaxValueValidator(100)], blank=True, null=True)

    regional_cuisines = models.ManyToManyField(Cuisine, blank=True)
    dining_vibes = models.ManyToManyField(DiningVibe, blank=True)
    dietary_needs = models.ManyToManyField(DietaryNeed, blank=True)
    budgets = models.ManyToManyField(Budget, blank=True)
    age_ranges = models.ManyToManyField(AgeRange, blank=True)

    def __str__(self):
        return self.user.username
