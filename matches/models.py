from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from user_page.models import UserProfile
from django.urls import reverse

class Match(models.Model):
    class Meta:
        verbose_name_plural='Matches'
        
    match_id = models.CharField(max_length=10, unique=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_initiator')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matched_user')

    user1_status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("accepted", "Accepted"), ("declined", "Declined")], default='pending')
    user2_status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("accepted", "Accepted"), ("declined", "Declined")], default='pending')

    def __str__(self):
        return self.user1.username+" "+self.user1_status+", "+self.user2.username+" "+self.user2_status
    
    
    def get_other_user(self, current_user):
        if current_user == self.user1:
            return self.user2
        elif current_user == self.user2:
            return self.user1
        return None  # fallback

    def get_accept_again_url(self):
        return reverse('matches:update_match_status', args=[self.match_id, 'accepted'])
