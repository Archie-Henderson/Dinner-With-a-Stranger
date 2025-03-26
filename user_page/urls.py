from django.urls import path
from . import views

urlpatterns = [
<<<<<<< Updated upstream
    path('me/', views.profile_home, name='profile_home'),
    path('me/edit/', views.edit_profile, name='edit_profile'),
    path('<int:user_id>/', views.view_profile, name='view_profile'),
=======
    path('profile/', views.profile_home, name='profile_home'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<username>/', views.view_profile, name='view_profile'),
    path('change-password/', views.change_password, name='change_password'),
>>>>>>> Stashed changes
]
