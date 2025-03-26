from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Match

def index(request):
    return render(request, 'index.html')

def match_list(request):
    matches = Match.objects.filter(user1=request.user)|Match.objects.filter(user2=request.user)
    return render(request, 'matches/match_list.html', {'matches': matches})

def match_detail(request, match_id):
    match = get_object_or_404(Match, match_id=match_id)
    return render(request, 'matches/match_detail.html', {'match': match})

def matches_pending(request):
    matches = Match.objects.filter(user1=request.user, user1_status='pending').exclude(user2_status='declined')|Match.objects.filter(user2=request.user, user2_status='pending').exclude(user1_status='declined')
    matches=matches.values()
    return render(request, 'matches/matches_pending.html', {'matches': matches})

def matches_accepted(request):
    matches = Match.objects.filter(user1=request.user, user1_status='accepted', user2_status='accepted')|Match.objects.filter(user2=request.user, user1_status='accepted', user2_status='accepted')
    matches=matches.values()
    return render(request, 'matches/matches_accepted.html', {'matches': matches})

def matches_denied(request):
    matches = Match.objects.filter(user1=request.user, user1_status='declined')|Match.objects.filter(user2=request.user, user1_status='declined')|Match.objects.filter(user1=request.user, user2_status='declined')|Match.objects.filter(user2=request.user, user2_status='declined')
    matches=matches.values()
    return render(request, 'matches/matches_denied.html', {'matches': matches})

def block_confirm(request):
    return render(request, 'matches/block_confirm.html')

def unmatch_confirm(request):
    return render(request, 'matches/unmatch_confirm.html')