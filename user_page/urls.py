from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_home, name='profile_home'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.CustomPasswordChangeView.as_view(), name='change_password'),  # Add password change view
    path('profile/<username>/', views.view_profile, name='view_profile'),
]
