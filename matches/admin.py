from django.contrib import admin
from matches.models import UserProfile, Match

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Match)