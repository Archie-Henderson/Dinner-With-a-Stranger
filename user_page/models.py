from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    description = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=20, unique=True)
    age = models.IntegerField(validators=[MinValueValidator(16), MaxValueValidator(100)])
    max_age_difference = models.PositiveIntegerField(validators=[MaxValueValidator(20)])

    def __str__(self):
        return self.user.username
