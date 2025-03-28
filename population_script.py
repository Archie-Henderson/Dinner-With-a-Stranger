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

def generate_random_match_id():
    return get_random_string(length=30).upper()

def assign_random_preferences(profile):
    profile.regional_cuisines.set(random.sample(list(Cuisine.objects.all()), k=min(2, Cuisine.objects.count())))
    profile.dining_vibes.set(random.sample(list(DiningVibe.objects.all()), k=min(2, DiningVibe.objects.count())))
    profile.dietary_needs.set(random.sample(list(DietaryNeed.objects.all()), k=min(2, DietaryNeed.objects.count())))
    profile.budgets.set(random.sample(list(Budget.objects.all()), k=1))
    profile.age_ranges.set(random.sample(list(AgeRange.objects.all()), k=1))
    profile.save()

def populate_users():
    users_data = [
        {
            'username': f'user{i}',
            'email': f'user{i}@example.com',
            'age': random.randint(18, 35),
            'description': f"User {i}'s bio",
            'phone_number': f'0123456789{i}',
        }
        for i in range(30)
    ]

    users = []
    for data in users_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            email=data['email'],
            defaults={'password': make_password('password123')}
        )
        if created:
            profile = UserProfile.objects.create(
                user=user,
                age=data['age'],
                description=data['description'],
                phone_number=data['phone_number']
            )
            assign_random_preferences(profile)
            print(f"Created user: {user.username}")
        else:
            print(f"ℹUser already exists: {user.username}")
        users.append(user)

    return users

def populate_matches(users):
    for user1 in users:
        # Random number of matches per user
        number_of_matches = random.randint(0, 10)

        # Choose random other users to match with (excluding themselves)
        potential_users = [u for u in users if u != user1]
        matched_users = random.sample(potential_users, min(number_of_matches, len(potential_users)))

        for user2 in matched_users:
            # Prevent duplicate match (user1-user2 and user2-user1)
            if Match.objects.filter(
                (Q(user1=user1) & Q(user2=user2)) | (Q(user1=user2) & Q(user2=user1))
            ).exists():
                continue

            match_id = generate_random_match_id()

            # Status assignment logic
            user1_status = random.choice(['pending', 'accepted', 'declined'])
            user2_status = random.choice(['pending', 'accepted'])

            if user1_status == 'declined' or user2_status == 'declined':
                user1_status = 'declined'
                user2_status = 'declined'
            elif user1_status == 'accepted' or user2_status == 'accepted':
                user1_status = 'accepted'
                user2_status = 'accepted'

            Match.objects.create(
                match_id=match_id,
                user1=user1,
                user2=user2,
                user1_status=user1_status,
                user2_status=user2_status,
            )

            print(f"Created match: {user1.username} ({user1_status}) & {user2.username} ({user2_status}), ID: {match_id}")


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

    print("Population complete.")
