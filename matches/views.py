from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings

from matches.models import Match
from user_page.models import UserProfile
from django.db.models import Q

from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect


def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

def find_new_matches(request):
    user=request.user
    user_profile=get_object_or_404(UserProfile, user=user)

    new_matches=0

    for other_user in UserProfile.objects.all():
        if not (Match.objects.filter(user1=user, user2=other_user) or Match.objects.filter(user1=other_user, user2=user)):
            if other_user.age < user.age+user.max_age_difference and other_user.age > user.age-user.max_age_difference and user.age < other_user.age+other_user.max_age_difference and user.age > other_user.age-other_user.max_age_difference:
                Match.objects.create(user1=user, user2=other_user)
                new_matches+=1
                if new_matches>50:
                    return

def index(request):
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

def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out. Hope you had a good Dining with Strangers!")
    return redirect('index')  # Redirect to the home page

