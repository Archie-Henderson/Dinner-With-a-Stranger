from matches.models import Match
from user_page.models import UserProfile
from django.db.models import Q

def check_matched(user_profile, other_profile):
    return not Match.objects.filter(
        Q(user1=user_profile.user, user2=other_profile.user) | 
        Q(user1=other_profile.user, user2=user_profile.user)
    ).exists()

def check_age_range(profile1, profile2):
    user_ranges = set(profile1.age_ranges.values_list('label', flat=True))
    other_ranges = set(profile2.age_ranges.values_list('label', flat=True))

    def in_range(age, ranges):
        for r in ranges:
            if r == '27+' and age >= 27:
                return True
            parts = r.split('-')
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                if int(parts[0]) <= age <= int(parts[1]):
                    return True
        return False

    return in_range(profile1.age, other_ranges) and in_range(profile2.age, user_ranges)

def check_cuisines_vibes(user, other_user):
    user_cuisines = set(user.regional_cuisines.values_list('name', flat=True))
    other_cuisines = set(other_user.regional_cuisines.values_list('name', flat=True))

    user_vibes = set(user.dining_vibes.values_list('name', flat=True))
    other_vibes = set(other_user.dining_vibes.values_list('name', flat=True))

    cuisines_match = bool(user_cuisines & other_cuisines)
    vibes_match = bool(user_vibes & other_vibes)

    return cuisines_match or vibes_match

#def find_new_matches(request):
#    matches=[]
#    for other_user in UserProfile.objects.exclude(user=request.user):
#        if check_age_range(request.user, other_user) and not check_matched(request.user, other_user) and check_cuisines(request.user, other_user):
#            matches.append(Match.objects.create(user1=request.user, user2=other_user))
#
#   return matches