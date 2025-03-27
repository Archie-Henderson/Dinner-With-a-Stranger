from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.conf import settings
from .models import Match


def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)


def index(request):
    return render(request, 'matches/index.html')

@login_required
def matches_pending(request):
    matches = Match.objects.filter(
        Q(user1=request.user) | Q(user2=request.user), 
        Q(user1_status='pending') | Q(user2_status='pending')
    ).exclude(Q(user1_status='declined') | Q(user2_status='declined')).values()
    return render(request, 'matches/matches_pending.html', {'matches': matches})

@login_required
def matches_accepted(request):
    matches = Match.objects.filter(Q(user1=request.user) | Q(user2=request.user),
        user2_status='accepted', user1_status='accepted').values()
    return render(request, 'matches/matches_accepted.html', {'matches': matches})


@login_required
def matches_denied(request):
    matches = Match.objects.filter(
        (Q(user1=request.user) & (Q(user1_status='declined') | Q(user2_status='declined'))) |
        (Q(user2=request.user) & (Q(user1_status='declined') | Q(user2_status='declined')))
    )
    return render(request, 'matches/matches_denied.html', {'matches': matches})


@staff_required(login_url='../possible/')
def matches_possible(request):
    matches = Match.objects.all()
    return render(request, 'matches/matches_possible.html', {'matches': matches})

@login_required
def block_confirm(request):
    return render(request, 'matches/block_confirm.html')

@login_required
def unmatch_confirm(request):
    return render(request, 'matches/unmatch_confirm.html')

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
