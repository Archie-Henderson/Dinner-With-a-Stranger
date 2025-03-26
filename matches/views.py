from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Q
from .models import Match

#Function to allow view to require staff permission to access
def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

# Home page
def index(request):
    return render(request, 'index.html')

# List all matches (for dev/testing)
@login_required
def match_list(request):
    matches = Match.objects.filter(user1=request.user)|Match.objects.filter(user2=request.user)
    return render(request, 'matches/match_list.html', {'matches': matches})

# Show details of a specific match
@login_required
def match_detail(request, match_id):
    match = get_object_or_404(Match, match_id=match_id)
    return render(request, 'matches/match_detail.html', {'match': match})

# Show pending matches involving current user
@login_required
def matches_pending(request):
    matches = Match.objects.filter(
        Q(user1=request.user, user1_status='pending') |
        Q(user2=request.user, user2_status='pending')
    ).exclude(Q(user1_status='declined')|Q(user2_status='declined')).values()
    return render(request, 'matches/matches_pending.html', {'matches': matches})

# Show accepted matches involving current user
@login_required
def matches_accepted(request):
    matches = Match.objects.filter(Q(user1=request.user)|Q(user2=request.user),
         user2_status='accepted', user1_status='accepted').values()    
    return render(request, 'matches/matches_accepted.html', {'matches': matches})

# Show matches that the current user has denied
@login_required
def matches_denied(request):
    matches = Match.objects.filter(
        Q(user1=request.user, user1_status='declined') |
        Q(user2=request.user, user2_status='declined')
    )
    return render(request, 'matches/matches_denied.html', {'matches': matches})



# Show all current matches made (staff only)
@staff_required(login_url="../admin")
def matches_possible(request):
    matches = Match.objects.all()
    return render(request, 'matches/matches_possible.html', {'matches': matches})

# Confirm block view (could be after user blocks someone)
@login_required
def block_confirm(request):
    return render(request, 'matches/block_confirm.html')

# Confirm unmatch view
@login_required
def unmatch_confirm(request):
    return render(request, 'matches/unmatch_confirm.html')

# Base layout test or section hub
@login_required
def matches_base(request):
    return render(request, 'matches/matches_base.html')

# Update a match's status (e.g., accept or decline) — useful for AJAX
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
