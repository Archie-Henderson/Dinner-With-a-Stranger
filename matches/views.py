from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.urls import reverse

from matches.models import Match
from user_page.models import UserProfile
from django.db.models import Q
#from user_page.forms import UserPreferencesForm  

from django.contrib import messages
from django.contrib.auth import logout


def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

def __check_matched(user, other_user):
    if not (Match.objects.filter(user1=user, user2=other_user) or Match.objects.filter(user1=other_user, user2=user)):
        return True
    else:
        return False

def __check_age_range(user, other_user):
    if ((user.age_range=='27+' and other_user.age>=27) or (other_user.age < int(user.age_range[-2:]) and other_user.age > int(user.age_range[:2]))) and ((other_user.age_range=='27+' and user.age>=27) or (user.age < int(other_user.age_range[-2:]) and user.age > int(other_user.age_range[:2]))):
        return True
    else:
        return False
    
def __check_cuisines(user, other_user):
    for cuisine in user.cuisines:
        if cuisine in other_user.cuisines:
            return True
        
    return False

def find_new_matches(request):
    user=request.user
    user_profile=get_object_or_404(UserProfile, user=user)

    new_matches=0

    for other_user in UserProfile.objects.all():
        if __check_matched(user,other_user) and __check_age_range(user,other_user) and __check_cuisines(user, other_user):
            Match.objects.create(user1=user, user2=other_user)
            new_matches+=1
            if new_matches>50:
                return

def index(request):
    if not request.user.is_authenticated and 'logged_out' not in request.session:
        messages.info(request, "You've logged out successfully!")
        request.session['logged_out'] = True  # Mark the session to ensure the message appears once
    return render(request, 'matches/index.html')

@login_required
def matches_pending(request):
    matches = Match.objects.filter(
        Q(user1=request.user, user1_status='accepted', user2_status='pending') | 
        Q(user2=request.user, user2_status='accepted', user1_status='pending')
        )
    return render(request, 'matches/matches_pending.html', {'matches': matches})

@login_required
def ajax_matches_pending(request):
    matches = Match.objects.filter(
        Q(user1=request.user) | Q(user2=request.user), 
        Q(user1_status='pending') | Q(user2_status='pending')
    ).exclude(
        Q(user1_status='declined') | Q(user2_status='declined')
    ).values()  
    return JsonResponse({'matches': list(matches)})


@login_required
def matches_accepted(request):
    matches = Match.objects.filter(Q(user1=request.user) | Q(user2=request.user),
        user2_status='accepted', user1_status='accepted')
    return render(request, 'matches/matches_accepted.html', {'matches': matches})


@login_required
def matches_denied(request):
    matches = Match.objects.filter(
        (Q(user1=request.user) & (Q(user1_status='declined') | Q(user2_status='declined'))) |
        (Q(user2=request.user) & (Q(user1_status='declined') | Q(user2_status='declined')))
    )
    return render(request, 'matches/matches_denied.html', {'matches': matches})


@login_required
def matches_possible(request):
    try:
        matches = Match.objects.filter(
            Q(user1=request.user, user1_status='pending') | 
            Q(user2=request.user, user2_status='pending')
            ).exclude(Q(user1_status='declined') | Q(user2_status='declined'))
    
    except:
        find_new_matches(request)
        matches = Match.objects.filter(
            Q(user1=request.user, user1_status='pending') | 
            Q(user2=request.user, user2_status='pending')
            ).exclude(Q(user1_status='declined') | Q(user2_status='declined'))
        
    return render(request, 'matches/matches_possible.html', {'matches': matches})

@login_required
def matches_base(request):
    return render(request, 'matches/matches_base.html')

# Update match status for the current user (for AJAX or link buttons)
@login_required
def update_match_status(request, match_id, decision):
    match = get_object_or_404(Match, match_id=match_id)

    if decision not in ['accepted', 'declined', 'pending']:
        return JsonResponse({'error': 'Invalid status'}, status=400)

    if request.user == match.user1:
        match.user1_status = decision
    elif request.user == match.user2:
        match.user2_status = decision
    else:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    match.save()
    return JsonResponse({'status': 'updated', 'match_id': match_id})

@login_required
def match_action_confirm(request, match_id, action_type):
    match = get_object_or_404(Match, match_id=match_id)
    
    if action_type not in ['deny', 'unmatch']:
        return HttpResponse("Invalid action", status=400)

    other_user = match.user1 if match.user2 == request.user else match.user2

    return render(request, 'matches/match_action_confirm.html', {
        'other_user': other_user,
        'match': match,
        'action_type': action_type,  # Pass the action type (deny/unmatch)
    })

#for the match count on the index page
def total_matches(request):
    count = Match.objects.count()
    return JsonResponse({'total_matches': count})


@login_required
def user_match_counts(request):
    user = request.user
    possible_count = Match.objects.filter(user=user,status="possible").count()
    accepted_count = Match.objects.filter(user=user,status="accepted").count()
    pending_count = Match.objects.filter(user=user, status="pending").count()
    denied_count = Match.objects.filter(user=user, status="denied").count()

    return JsonResponse({
        'possible': possible_count,
        'accepted': accepted_count,
        'pending': pending_count,
        'denied' : denied_count
    })

def toggle_theme(request):
    """
    Toggle the theme (dark/light) based on the AJAX POST request.
    Sets a cookie named 'theme' with the new value.
    """
    if request.method == 'POST' and request.is_ajax():
        new_theme = request.POST.get('theme', 'light')
        response = JsonResponse({'status': 'success', 'theme': new_theme})
        # Set cookie for 30 days (adjust max_age as needed)
        response.set_cookie('theme', new_theme, max_age=30*24*60*60)
        return response
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


# def registration_preferences(request):
#     user_profile, created = UserProfile.objects.get_or_create(user=request.user)

#     if request.method == "POST":
#         form = UserPreferencesForm(request.POST, instance=user_profile)
#         if form.is_valid():
#             form.save()
#             return redirect('matches_possible')  
#         form = UserPreferencesForm(instance=user_profile)

#     return render(request, 'registration_preferences.html', {'form': form})