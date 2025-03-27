import random
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dinner_with_a_stranger.settings')

import django
django.setup()

from django.contrib.auth.models import User
from matches.models import Match
from user_page.models import UserProfile
from django.utils.crypto import get_random_string

# Set up Django environment

def generate_random_match_id():
    # Generate a random match_id for the match (unique string)
    return get_random_string(length=10).upper()

def populate_users():
    # List of fake users to add
    users_data = [{'username': f'user{i}', 'email': f'user{i}@example.com', 'age': random.randint(18, 35), 'description': f"User {i}'s bio", 'phone_number': f'0123456789{i}', 'max_age_difference':10}for i in range(10)]

    # Add users to the database
    for user_data in users_data:
        print(user_data['username'], user_data['email'])
        user, created = User.objects.get_or_create(username=user_data['username'], email=user_data['email'])
        if created:
            # Create a UserProfile for each user
            UserProfile.objects.create(user=user, age=user_data['age'], description=user_data['description'], phone_number=user_data['phone_number'], max_age_difference=user_data['max_age_difference'])
            print(f"Created user: {user.username}")
        else:
            print(f"User already exists: {user.username}")
   
    return User.objects.all()

def populate_matches(users):
    # Generate random matches between users
    for i in range(9):  # Create 9 matches
        user1 = User.objects.get(username=f'user{i}')
        user2 = User.objects.get(username=f'user{i+1}')
       
        # Randomly assign statuses for user1 and user2
        user1_status = random.choice(['pending', 'accepted', 'declined'])
        user2_status = random.choice(['pending', 'accepted', 'declined'])
       
        # Generate a unique match_id
        match_id = generate_random_match_id()
       
        # Create match
        match = Match.objects.create(
            match_id=match_id,
            user1=user1,
            user2=user2,
            user1_status=user1_status,
            user2_status=user2_status
        )
        print(f"Created match between {user1.username} and {user2.username}, match_id: {match_id}")

# Start execution here! because above this point, we define functions; these are not executed unless we call them.
if __name__ == '__main__':
    print('Starting population script...')
    users = populate_users()  # Create users
    populate_matches(users)   # Create matches
    print('Population complete.')