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
    # List of fake users to add
    users_data = [{'username': f'user{i}', 'email': f'user{i}@example.com', 'age': random.randint(18, 35), 'description': f"User {i}'s bio", 'phone_number': f'0123456789{i}'}for i in range(30)]

    # Add users to the database
    for user_data in users_data:
        print(user_data['username'], user_data['email'])
        user, created = User.objects.get_or_create(username=user_data['username'], email=user_data['email'])
        if created:
            # Create a UserProfile for each user
            UserProfile.objects.create(user=user, age=user_data['age'], description=user_data['description'], phone_number=user_data['phone_number'],)
            print(f"Created user: {user.username}")
        else:
            print(f"User already exists: {user.username}")
    
    return User.objects.all()

def populate_matches(users):
    created_pairs = set()

    for user in users:
        # Decide how many matches to create for this user
        num_matches = random.randint(3, 10)
        other_users = random.sample([u for u in users if u != user], k=min(num_matches, len(users) - 1))

        for other_user in other_users:
            # Prevent duplicates (A-B and B-A)
            pair = tuple(sorted([user.id, other_user.id]))
            if pair in created_pairs:
                continue
            created_pairs.add(pair)

            match_id = get_random_string(30).upper()

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

            Match.objects.create(
                match_id=match_id,
                user1=user,
                user2=other_user,
                user1_status=user1_status,
                user2_status=user2_status,
            )
            print(f"Created match: {user.username} ({user1_status}) & {other_user.username} ({user2_status}), ID: {match_id}")


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
