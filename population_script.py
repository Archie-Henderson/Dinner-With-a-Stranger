import random
import os
from django.db.models import Q
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dinner_with_a_stranger.settings')

import django
django.setup()

from django.contrib.auth.models import User
from matches.models import Match
from user_page.models import (
    UserProfile, Cuisine, DiningVibe, DietaryNeed, Budget, AgeRange
)
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password

from django.core.files import File

def generate_random_match_id():
    return get_random_string(length=30).upper()

def assign_random_preferences(profile):
    profile.regional_cuisines.set(random.sample(list(Cuisine.objects.all()), k=min(3, Cuisine.objects.count())))
    profile.dining_vibes.set(random.sample(list(DiningVibe.objects.all()), k=min(3, DiningVibe.objects.count())))
    profile.dietary_needs.set(random.sample(list(DietaryNeed.objects.all()), k=min(2, DietaryNeed.objects.count())))
    profile.budgets.set(random.sample(list(Budget.objects.all()), k=1))
    profile.age_ranges.set(random.sample(list(AgeRange.objects.all()), k=1))
    profile.save()

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

def check_cuisines(user, other_user):
    user_cuisines = set(user.regional_cuisines.values_list('name', flat=True))
    other_cuisines = set(other_user.regional_cuisines.values_list('name', flat=True))
    return bool(user_cuisines & other_cuisines)

def populate_users():
    users_data = [{'username': f'user{i}', 'email': f'user{i}@example.com', 'age': random.randint(18, 35), 'description': f"User {i}'s bio", 'phone_number': f'0123456789{i}'} for i in range(50)]

    pictures_folder = 'media/profile_images/'
    picture_files = [f"user-pic-{i+1}.jpg" for i in range(50)]

    created_users = []  # ← add this

    for user_data, picture_filename in zip(users_data, picture_files):
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            email=user_data['email'],
            defaults={'password': make_password('password123')}
        )
        if created:
            profile = UserProfile.objects.create(
                user=user,
                age=user_data['age'],
                description=user_data['description'],
                phone_number=user_data['phone_number'],
            )
            picture_path = os.path.join(pictures_folder, picture_filename)
            with open(picture_path, 'rb') as f:
                profile.picture.save(os.path.basename(picture_path), File(f))
            assign_random_preferences(profile)
            print(f"Created user: {user.username} with picture {picture_filename}")
        else:
            print(f"User already exists: {user.username}")

        created_users.append(user)  # ← collect user

    return created_users  # ← return the list


def populate_matches(users):
    created_pairs = set()
    count_created = 0

    profiles = {user.id: UserProfile.objects.get(user=user) for user in users}

    for user in users:
        for other_user in users:
            if user == other_user:
                continue

            pair = tuple(sorted([user.id, other_user.id]))
            if pair in created_pairs:
                continue

            user_profile = profiles[user.id]
            other_profile = profiles[other_user.id]

            # Check if they match preferences
            if check_age_range(user_profile, other_profile) and check_cuisines(user_profile, other_profile):
                # 50% chance → create match
                if random.random() < 0.3:
                    roll = random.random()
                    if roll < 0.15:
                        user1_status = 'accepted'
                        user2_status = 'accepted'
                    elif roll < 0.75:
                        if random.choice([True, False]):
                            user1_status = 'accepted'
                            user2_status = 'pending'
                        else:
                            user1_status = 'pending'
                            user2_status = 'accepted'
                    else:
                        user1_status = 'declined'
                        user2_status = 'declined'

                    match_id = get_random_string(30).upper()
                    Match.objects.create(
                        match_id=match_id,
                        user1=user,
                        user2=other_user,
                        user1_status=user1_status,
                        user2_status=user2_status,
                    )
                    print(f"Created match: {user.username} ({user1_status}) & {other_user.username} ({user2_status})")
                    count_created += 1

                # Else: no match → will appear in possible suggestions

            created_pairs.add(pair)

    print(f"\n Total matches created: {count_created}")

def populate_preference_options():
    Cuisine.objects.bulk_create([
        Cuisine(name="Asian"),
        Cuisine(name="Italian"),
        Cuisine(name="Mediterranean"),
        Cuisine(name="Indian"),
        Cuisine(name="Latin American"),
    ], ignore_conflicts=True)

    DiningVibe.objects.bulk_create([
        DiningVibe(name="Fast Food"),
        DiningVibe(name="Fine Dining"),
        DiningVibe(name="Healthy & Organic"),
        DiningVibe(name="Brunch & Breakfast"),
        DiningVibe(name="Café & Coffee"),
    ], ignore_conflicts=True)

    DietaryNeed.objects.bulk_create([
        DietaryNeed(name="Vegetarian"),
        DietaryNeed(name="Vegan"),
        DietaryNeed(name="Keto / Low-carb"),
        DietaryNeed(name="Gluten-free"),
        DietaryNeed(name="Nut Allergy"),
        DietaryNeed(name="Lactose Intolerant"),
        DietaryNeed(name="Pescatarian"),
        DietaryNeed(name="No Restrictions"),
    ], ignore_conflicts=True)

    Budget.objects.bulk_create([
        Budget(level="$"),
        Budget(level="$$"),
        Budget(level="$$$"),
        Budget(level="$$$$"),
    ], ignore_conflicts=True)

    AgeRange.objects.bulk_create([
        AgeRange(label="16-19"),
        AgeRange(label="19-21"),
        AgeRange(label="21-23"),
        AgeRange(label="24-26"),
        AgeRange(label="27+"),
    ], ignore_conflicts=True)

if __name__ == '__main__':
    populate_preference_options()
    users = populate_users()
    populate_matches(users)
    print("\n Population complete!")
