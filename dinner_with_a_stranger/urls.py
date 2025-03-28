"""dinner_with_a_stranger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy 
from matches import views as match_views
from user_page import views as user_page_views

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', match_views.index, name='index'),
    path('matches/', include('matches.urls')),
    path('profile/', include('user_page.urls')), 
    path('admin/', admin.site.urls),
    # path('accounts/register/', CreateView.as_view(
    #     template_name='registration/registration_form.html',
    #     form_class=UserCreationForm,
    #     success_url=reverse_lazy('matches_possible')
    #     ), name='register'),
    path('accounts/', include('registration.backends.simple.urls')),
    path('toggle_theme/', match_views.toggle_theme, name='toggle_theme'),
    path('preferences/', user_page_views.registration_preferences, name='registration_preferences'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

