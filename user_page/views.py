from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .forms import ProfileEditForm  # Import the form you just created

# Display the current user's profile
@login_required
def profile_home(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'userpage/user_profile.html', {'profile': profile})

# Edit the current user's profile using the form
@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile_home')  # Redirect to the profile view after saving
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'userpage/user_profile_edit.html', {'form': form})

# Change the user's password (Placeholder for password change view)
@login_required
def change_password(request):
    # Password change logic goes here (usually handled with Django's built-in forms)
    return render(request, 'userpage/change_password.html')

# View another user's profile by username
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=user)
    return render(request, 'userpage/view_profile.html', {
        'view_user': user,
        'profile': profile,
    })
