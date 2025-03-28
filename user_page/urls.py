from django.urls import path
from . import views

app_name = 'user_page'

urlpatterns = [
    path('', views.profile_home, name='profile_home'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('<username>/', views.view_profile, name='view_profile'),
    path('profile/<int:user_id>/', views.view_user_profile, name='view_user_profile')
]
