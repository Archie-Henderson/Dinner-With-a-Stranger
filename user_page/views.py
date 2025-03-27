from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.views import PasswordChangeView

from django.contrib.auth.models import User  
from matches.models import Match
from .models import UserProfile
from django.db.models import Q

from .forms import EditProfileForm

@login_required
def profile_home(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    
    return render(request, 'userpage/user_profile.html', {
            'view_user': request.user,
            'profile': profile,
            'is_own_profile': True,
            'allow_view':True
        })

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

# View another user's profile by username
@login_required
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=user)

    # Check if the current user is viewing their own profile or another user's
    is_own_profile = request.user == user

    # Logic to check if the current user has permission to view the profile
    try:
        match = Match.objects.get(Q(user1=request.user, user2=user) | Q(user2=request.user, user1=user))
        
        # If either user has declined the match, don't allow the view
        if match.user1_status == 'declined' or match.user2_status == 'declined':
            allow_view = False
        else:
            allow_view = True
    except:
        allow_view = False

    return render(request, 'userpage/user_profile.html', {
        'profile': profile,
        'is_own_profile': is_own_profile,
        'view_user': user,
        'allow_view': allow_view,
    })
