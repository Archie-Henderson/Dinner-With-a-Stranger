import os
import random
import django
from django.contrib.auth.models import User
from matches.models import Match
from user_page.models import UserProfile
from django.utils.crypto import get_random_string

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dinner_with_a_stranger.settings')
django.setup()

def generate_random_match_id():
    # Generate a random match_id for the match (unique string)
    return get_random_string(length=10).upper()

def populate_users():
    # List of fake users to add
    users_data = [
        {'username': 'user1', 'email': 'user1@example.com', 'age': random.randint(18, 35), 'bio': "User 1's bio"},
        {'username': 'user2', 'email': 'user2@example.com', 'age': random.randint(18, 35), 'bio': "User 2's bio"},
        {'username': 'user3', 'email': 'user3@example.com', 'age': random.randint(18, 35), 'bio': "User 3's bio"},
        {'username': 'user4', 'email': 'user4@example.com', 'age': random.randint(18, 35), 'bio': "User 4's bio"},
        {'username': 'user5', 'email': 'user5@example.com', 'age': random.randint(18, 35), 'bio': "User 5's bio"},
        {'username': 'user6', 'email': 'user6@example.com', 'age': random.randint(18, 35), 'bio': "User 6's bio"},
        {'username': 'user7', 'email': 'user7@example.com', 'age': random.randint(18, 35), 'bio': "User 7's bio"},
        {'username': 'user8', 'email': 'user8@example.com', 'age': random.randint(18, 35), 'bio': "User 8's bio"},
        {'username': 'user9', 'email': 'user9@example.com', 'age': random.randint(18, 35), 'bio': "User 9's bio"},
        {'username': 'user10', 'email': 'user10@example.com', 'age': random.randint(18, 35), 'bio': "User 10's bio"},
    ]
   
    # Add users to the database
    for user_data in users_data:
        user, created = User.objects.get_or_create(username=user_data['username'], email=user_data['email'])
        if created:
            # Create a UserProfile for each user
            UserProfile.objects.create(user=user, age=user_data['age'], bio=user_data['bio'])
            print(f"Created user: {user.username}")
        else:
            print(f"User already exists: {user.username}")
   
    return User.objects.all()

def populate_matches(users):
    # Generate random matches between users
    for i in range(10):  # Create 10 random matches
        user1, user2 = random.sample(users, 2)
       
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