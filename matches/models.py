from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    description = models.CharField(max_length=200, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.user.username


class Match(models.Model):
    match_id = models.CharField(max_length=10, unique=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE)

    user1_status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("accepted", "Accepted"), ("declined", "Declined")])
    user2_status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("accepted", "Accepted"), ("declined", "Declined")])

    def __str__(self):
        return self.user1.username+" "+self.user1_status+", "+self.user2.username+" "+self.user2_status