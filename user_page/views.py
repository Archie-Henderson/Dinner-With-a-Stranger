from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from django.contrib.auth.views import PasswordChangeView

from django.contrib.auth.models import User  
from matches.models import Match
from user_page.models import UserProfile
from django.db.models import Q

from user_page.forms import EditProfileForm

@login_required
def profile_home(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    
    return render(request, 'user_page/user_profile.html', {
            'view_user': request.user,
            'profile': profile,
            'is_own_profile': True,
            'allow_view':True
        })

@login_required
def edit_profile(request):

    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)  
        if form.is_valid():
            form.save()
            return redirect('user_page:profile_home')
    else:
        form = EditProfileForm(instance=profile)  
    
    return render(request, 'user_page/user_profile_edit.html', {'form': form})

def registration_preferences(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user=User.objects.get(username=request.user.username)

            description=form['description']
            age=form['age']
            picture=form['picture']
            phone_number=form['phone_number']
            regional_cuisines=form['regional_cuisines']
            dining_vibes=form['dining_vibes']
            budgets=form['budgets']
            age_ranges=form['age_ranges']
            dietary_needs=form['dietary_needs']
            UserProfile.objects.create(user=user,description=description,age=age,picture=picture,phone_number=phone_number,
                                       regional_cuisines=regional_cuisines,dining_vibes=dining_vibes,
                                       budgets=budgets,age_ranges=age_ranges,dietary_needs=dietary_needs)
            return redirect(reverse('matches:matches_possible'))  # Redirect to matches page after preferences
        else:
            redirect(reverse('user_page:profile_home'))
    else:
        form = EditProfileForm()

    return render(request, 'registration/registration_preferences.html', {
        'form': form,
        'is_new_user': True
    })


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'userpage/change_password.html'
    success_url = '/profile/'  

# View another user's profile by username
@login_required
def view_profile(request, username=None):
    if username==None:
        user=request.user
    else:    
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

    return render(request, 'user_page/user_profile.html', {
        'profile': profile,
        'is_own_profile': is_own_profile,
        'view_user': user,
        'allow_view': allow_view,
    })

@login_required
def view_user_profile(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    match = Match.objects.filter(
        (Q(user1=request.user, user2=other_user) | Q(user1=other_user, user2=request.user)),
        user1_status='accepted',
        user2_status='accepted'
    ).first()

    if not match:
        return HttpResponse("You are not matched with this user.", status=403)

    return render(request, 'user_page/other_user_profile.html', {'other_user': other_user})
