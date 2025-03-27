from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
<<<<<<< HEAD
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User  
from .models import UserProfile
from .forms import ProfileEditForm

=======
from django.db.models import Q

from matches.models import Match
from user_page.models import UserProfile
from django.contrib.auth.models import User

from user_page.forms import EditProfileForm  # Import the form you just created
>>>>>>> 68f07454a925b6106a0ec99b5bd32b3cc08eb5f9

@login_required
def profile_home(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'userpage/user_profile.html', {'profile': profile, 'is_own_profile': True})

@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile_home')  
    else:
        form = EditProfileForm(instance=profile)

    return render(request, 'userpage/user_profile_edit.html', {'form': form})

<<<<<<< HEAD
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'userpage/change_password.html'
    success_url = '/profile/'  

=======
# View another user's profile by username
@login_required
>>>>>>> 68f07454a925b6106a0ec99b5bd32b3cc08eb5f9
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=user)

<<<<<<< HEAD
    is_own_profile = request.user == user

    return render(request, 'userpage/user_profile.html', {
        'profile': profile,
        'is_own_profile': is_own_profile,
        'view_user': user  
    })
=======
    try:
        match=Match.objects.get(Q(user1=request.user,user2=user) | Q(user2=request.user,user1=user))
        
        if match.user1_status=='declined' or match.user2_status=='declined':
            allow_view=False
        else:
            allow_view=True
    except:
        allow_view=False
    finally:

        return render(request, 'userpage/view_profile.html', {
            'view_user': user,
            'profile': profile,
            'allow_view':allow_view
        })
    
>>>>>>> 68f07454a925b6106a0ec99b5bd32b3cc08eb5f9
