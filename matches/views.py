from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from matches.models import Match
from user_page.models import UserProfile
from django.contrib.auth.models import User 
from django.db.models import Q

from django.contrib import messages

from django.views.decorators.http import require_POST

from django.utils.crypto import get_random_string

from matches.helpers import check_matched, check_age_range, check_cuisines_vibes

def index(request):
    if not request.user.is_authenticated and 'logged_out' not in request.session:
        messages.info(request, "You've logged out successfully!")
        request.session['logged_out'] = True  # Mark the session to ensure the message appears once
    return render(request, 'matches/index.html')


@login_required
def matches_possible(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Exclude users who are either matched, accepted, or have declined the match
    excluded_users = Match.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).values_list('user1', 'user2')

    # Flatten the list of user IDs to exclude
    flat_excluded_ids = set()
    for u1, u2 in excluded_users:
        flat_excluded_ids.update([u1, u2])
    flat_excluded_ids.discard(request.user.id)

    # Get the list of possible matches (exclude users who are already excluded)
    possible_profiles = []
    for other_profile in UserProfile.objects.exclude(user=request.user).exclude(user__id__in=flat_excluded_ids):
        if check_age_range(user_profile, other_profile) and check_cuisines_vibes(user_profile, other_profile):
            possible_profiles.append(other_profile.user)

    return render(request, 'matches/matches_possible.html', {'possible_users': possible_profiles})

@login_required
def matches_pending(request):
    matches = Match.objects.filter(
        (Q(user1=request.user) & Q(user1_status='pending') & Q(user2_status='accepted')) |
        (Q(user2=request.user) & Q(user2_status='pending') & Q(user1_status='accepted'))
    )

    matches_with_others = [(match, match.get_other_user(request.user)) for match in matches]

    return render(request, 'matches/matches_pending.html', {
        'matches_with_others': matches_with_others
    })

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
    matches = Match.objects.filter(
        (Q(user1=request.user) | Q(user2=request.user)),
        user1_status='accepted',
        user2_status='accepted'
    )

    matches_with_others = [(match, match.get_other_user(request.user)) for match in matches]

    return render(request, 'matches/matches_accepted.html', {
        'matches_with_others': matches_with_others
    })

@login_required
def matches_denied(request):
    matches = Match.objects.filter(
        (Q(user1=request.user) & Q(user1_status='declined')) |
        (Q(user2=request.user) & Q(user2_status='declined'))
    )

    filtered = []
    for match in matches:
        if (match.user1 == request.user and match.user1_status == 'declined') or \
            (match.user2 == request.user and match.user2_status == 'declined'):
            filtered.append((match, match.get_other_user(request.user)))

    return render(request, 'matches/matches_denied.html', {
        'matches_with_others': filtered
    })


@login_required
def matches_base(request):
    return render(request, 'matches/matches_base.html')

@login_required
@require_POST
def update_match_status(request, match_id, status):
    if status not in ['accepted', 'declined']:
        return JsonResponse({'error': 'Invalid status'}, status=400)

    match = get_object_or_404(Match, match_id=match_id)

    acting_user = request.user
    other_user = match.user1 if match.user2 == acting_user else match.user2

    if status == 'accepted':
        if acting_user == match.user1:
            if match.user2_status == 'declined':
                match.user1_status = 'accepted'
                match.user2_status = 'pending'
            elif match.user2_status == 'accepted':
                match.user1_status = 'accepted'
                match.user2_status = 'accepted'
            elif match.user2_status == 'pending':
                match.user1_status = 'accepted'
                match.user2_status = 'accepted'
            else:
                match.user1_status = 'accepted'
                match.user2_status = 'pending'
        else:  # acting_user == match.user2
            if match.user1_status == 'declined':
                match.user2_status = 'accepted'
                match.user1_status = 'pending'
            elif match.user1_status == 'accepted':
                match.user1_status = 'accepted'
                match.user2_status = 'accepted'
            elif match.user1_status == 'pending':
                match.user1_status = 'accepted'
                match.user2_status = 'accepted'
            else:
                match.user2_status = 'accepted'
                match.user1_status = 'pending'

    elif status == 'declined':
        if acting_user == match.user1:
            if match.user2_status == 'pending':
                match.user1_status = 'declined'
                match.user2_status = 'denied'
            else:
                match.user1_status = 'declined'
        else:  # acting_user == match.user2
            if match.user1_status == 'pending':
                match.user2_status = 'declined'
                match.user1_status = 'denied'
            else:
                match.user2_status = 'declined'

    match.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@require_POST
def possible_match_accept(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if other_user == request.user:
        return HttpResponse("Cannot match yourself", status=400)

    match = Match.objects.filter(
        (Q(user1=request.user, user2=other_user) | Q(user1=other_user, user2=request.user))
    ).first()

    if match:
        return HttpResponse("Match already exists", status=400)

    match_id = get_random_string(30).upper()

    # Your status = accepted, their status = pending
    Match.objects.create(
        match_id=match_id,
        user1=request.user,
        user2=other_user,
        user1_status='accepted',
        user2_status='pending'
    )

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@require_POST
def possible_match_deny(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if other_user == request.user:
        return HttpResponse("Cannot decline yourself", status=400)

    match = Match.objects.filter(
        (Q(user1=request.user, user2=other_user) | Q(user1=other_user, user2=request.user))
    ).first()

    if match:
        if match.user1 == request.user:
            match.user1_status = 'declined'
        else:
            match.user2_status = 'declined'
        match.save()
    else:
        # No match yet → create
        match_id = get_random_string(30).upper()
        if request.user.id < other_user.id:
            Match.objects.create(
                match_id=match_id,
                user1=request.user,
                user2=other_user,
                user1_status='declined',
                user2_status='pending'
            )
        else:
            Match.objects.create(
                match_id=match_id,
                user1=other_user,
                user2=request.user,
                user1_status='pending',
                user2_status='declined'
            )

    return redirect('matches:matches_possible')

@login_required
def match_action_confirm(request, match_id, action_type):
    match = get_object_or_404(Match, match_id=match_id)

    # Check if the action is valid
    if action_type not in ['deny', 'unmatch', 'accept']:
        return HttpResponse("Invalid action", status=400)

    other_user = match.user1 if match.user2 == request.user else match.user2

    if action_type == 'accept':
        # If the user wants to accept, render the confirmation page
        if request.method == 'POST':
            # If it's a POST request, update the match status
            return redirect('matches:update_match_status', match_id=match.match_id, decision='accepted')
        return render(request, 'matches/match_accept_confirm.html', {
            'other_user': other_user,
            'match': match,
            'action_type': action_type,
        })

    # Handle other actions like deny or unmatch
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
    user_profile = get_object_or_404(UserProfile, user=user)

    # Possible matches calculation
    excluded_users = Match.objects.filter(
        Q(user1=user) | Q(user2=user)
    ).values_list('user1', 'user2')

    flat_excluded_ids = set()
    for u1, u2 in excluded_users:
        flat_excluded_ids.update([u1, u2])
    flat_excluded_ids.discard(user.id)

    possible_profiles = []
    for other_profile in UserProfile.objects.exclude(user=user).exclude(user__id__in=flat_excluded_ids):
        if check_age_range(user_profile, other_profile) and check_cuisines_vibes(user_profile, other_profile):
            possible_profiles.append(other_profile.user)

    possible_count = len(possible_profiles)

    accepted_count = Match.objects.filter(
        (Q(user1=user) | Q(user2=user)),
        user1_status='accepted',
        user2_status='accepted'
    ).count()

    denied_count = Match.objects.filter(
        (Q(user1=user) & Q(user1_status='declined')) |
        (Q(user2=user) & Q(user2_status='declined'))
    ).count()

    pending_count = Match.objects.filter(
        (Q(user1=user) & Q(user1_status='pending') & Q(user2_status='accepted')) |
        (Q(user2=user) & Q(user2_status='pending') & Q(user1_status='accepted'))
    ).count()

    return JsonResponse({
        'possible': possible_count,
        'accepted': accepted_count,
        'pending': pending_count,
        'denied': denied_count
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

@login_required
def ajax_matches_accepted(request):
    # Filter accepted matches for the current user.
    matches = Match.objects.filter(
        (Q(user1=request.user) & Q(user1_status='accepted')) |
        (Q(user2=request.user) & Q(user2_status='accepted'))
    ).values()
    return JsonResponse({'matches': list(matches)})


@login_required
def ajax_matches_denied(request):
    # Filter denied (declined) matches for the current user.
    matches = Match.objects.filter(
        (Q(user1=request.user) & Q(user1_status='declined')) |
        (Q(user2=request.user) & Q(user2_status='declined'))
    ).values()
    return JsonResponse({'matches': list(matches)})

@login_required
def view_user_profile(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    # Check if they are mutually accepted
    match = Match.objects.filter(
        (Q(user1=request.user, user2=other_user) | Q(user1=other_user, user2=request.user)),
        user1_status='accepted',
        user2_status='accepted'
    ).first()

    if not match:
        return HttpResponse("You are not matched with this user.", status=403)

    return render(request, 'user_page/other_user_profile.html', {'other_user': other_user})
