from django.urls import path
from user_page import views

app_name = 'userpage'

urlpatterns = [
    path('me/', views.profile_home, name='profile_home'),
    path('me/edit/', views.edit_profile, name='edit_profile'),
    path('<int:user_id>/', views.view_profile, name='view_profile'),
]
