from django.urls import path
from . import views

app_name = 'user_page'

urlpatterns = [
    path('profile/', views.profile_home, name='profile_home'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<username>/', views.view_profile, name='view_profile'),
]
