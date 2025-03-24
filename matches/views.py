from django.shortcuts import render, get_object_or_404
from .models import Match

def match_list(request):
    matches = Match.objects.all()
    return render(request, 'matches/match_list.html', {'matches': matches})

def match_detail(request, match_id):
    match = get_object_or_404(Match, match_id=match_id)
    return render(request, 'matches/match_detail.html', {'match': match})

def matches_pending(request):
    matches = Match.objects.filter(user1=request.user, user1_status='pending')
    return render(request, 'matches/matches_pending.html', {'matches': matches})

def matches_accepted(request):
    matches = Match.objects.filter(user1=request.user, user1_status='accepted')
    return render(request, 'matches/matches_accepted.html', {'matches': matches})

def matches_denied(request):
    matches = Match.objects.filter(user1=request.user, user1_status='declined')
    return render(request, 'matches/matches_denied.html', {'matches': matches})

def matches_possible(request):
    matches = Match.objects.all()  # Change this filter if needed
    return render(request, 'matches/matches_possible.html', {'matches': matches})

def block_confirm(request):
    return render(request, 'matches/block_confirm.html')

def unmatch_confirm(request):
    return render(request, 'matches/unmatch_confirm.html')

def matches_base(request):
    return render(request, 'matches/matches_base.html')
