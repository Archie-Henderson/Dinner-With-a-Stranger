from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User  
from .models import UserProfile
from .forms import ProfileEditForm


@login_required
def profile_home(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'userpage/user_profile.html', {'profile': profile, 'is_own_profile': True})

@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile_home')  
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'userpage/user_profile_edit.html', {'form': form})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'userpage/change_password.html'
    success_url = '/profile/'  

def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=user)

    is_own_profile = request.user == user

    return render(request, 'userpage/user_profile.html', {
        'profile': profile,
        'is_own_profile': is_own_profile,
        'view_user': user  
    })
