from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def profile_home(request):
    return render(request, 'userpage/base.html', {'section': 'home'})

@login_required
def edit_profile(request):
    return render(request, 'userpage/base.html', {'section': 'edit'})

def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'userpage/base.html', {
        'section': 'view',
        'view_user': user
    })
