from django.urls import path
from userpage import views

app_name = 'userpage'

urlpatterns = [
    path('', views.profile_home, name='profile_home'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('view/<str:username>/', views.view_profile, name='view_profile'),
]
