import os
import importlib
from django.urls import reverse, reverse_lazy
from django.contrib.auth.hashers import make_password
import population_script


from django.test import TestCase
from django.conf import settings
from django.test.client import Client

from django.contrib.auth.models import User
from user_page.models import UserProfile
from matches.models import Match

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

# Create your tests here.
class PageSetupTests(TestCase):
    def setUp(self):
        self.client=Client()
        self.user=User.objects.create_user('Test', 'example@gmail.com', 'password123')

        self.client.login(username='Test', password='password123')

        self.views_module = importlib.import_module('matches.views')
        self.views_module_listing = dir(self.views_module)
        
        self.project_urls_module = importlib.import_module('matches.urls')

        self.pages={'matches_pending':('pending/',self.views_module.matches_pending), 'matches_accepted':('accepted/',self.views_module.matches_accepted),'matches_denied':('denied/',self.views_module.matches_denied), 'matches_possible':('possible/',self.views_module.matches_possible), 'matches_base':('base/',self.views_module.matches_base), 'update_match_status':('update/10/y/',self.views_module.update_match_status)}

    def test_view_exists(self):
        for (page, values) in self.pages.items():

            name_exists = page in self.views_module_listing
            is_callable = callable(values[1])

            self.assertTrue(name_exists, f"{FAILURE_HEADER}The {page}() view for matches does not exist.{FAILURE_FOOTER}")
            self.assertTrue(is_callable, f"{FAILURE_HEADER}Check that you have created the {page}() view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")

    def test_mappings_exists(self):
        for (page, values) in self.pages.items():

            index_mapping_exists = False

            # This is overridden. We need to manually check it exists.
            for mapping in self.project_urls_module.urlpatterns:
                if hasattr(mapping, 'name'):
                    if mapping.name == page:
                        index_mapping_exists = True
                        break
        
            if page in ['match_detail','update_match_status']:
                args=['10']
                if page=='update_match_status':
                    args.append('y')

                self.assertEquals(reverse(f'matches:{page}', args=args), f'/matches/{values[0]}', f"{FAILURE_HEADER}The {page} URL lookup failed. Check matches' urls.py module.{FAILURE_FOOTER}")
            else:
                self.assertEquals(reverse(f'matches:{page}'), f'/matches/{values[0]}', f"{FAILURE_HEADER}The {page} URL lookup failed. Check matches' urls.py module.{FAILURE_FOOTER}")

            self.assertTrue(index_mapping_exists, f"{FAILURE_HEADER}The {page} URL mapping could not be found. Check matches' urls.py module.{FAILURE_FOOTER}")
            
    def test_response(self):        
        for (page, values) in self.pages.items():

            response = self.client.get(reverse(f'matches:{page}'))

            self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Requesting the {page} page failed. Check your URLs and view.{FAILURE_FOOTER}")

    def test_match_model(self):
        user1=User.objects.create(username='test1')
        user2=User.objects.create(username='test2')
        match1=Match.objects.get(user1=user1, user2=user2)
        self.assertEqual(match1.user1_status, 'pending')
        self.assertEqual(match1.user2_status, 'pending')

class PopulationScriptTest(TestCase):
    def setup(self):
        population_script.populate_users()
        population_script.populate_preference_options()
        population_script.populate_matches()
        population_script.assign_random_preferences()

    def test_users(self):
        users=User.objects.filter()
        users_len=len(users)
        users_strs=map(str,users)

        self.assertEqual(users_len, 50)
        for i in range(50):
            self.assertTrue(f'user{i}' in users_strs)
        
    def test_user_profiles(self):        
        profiles=UserProfile.objects.filter()
        profiles_len=len(profiles)
        profiles_str=map(str,profiles)

        self.assertEqual(profiles_len, 50)
        for i in range(50):
            self.assertTrue(f'user{i}' in profiles_str)
            self.assertTrue(f"User {i}'s bio" == profiles[i].description)

    def test_matches(self):
        matches=Match.objects.all()
        matches_len=len(matches)

        self.assertEquals(matches_len, 100)

class ViewTests(TestCase):
    def setUp(self):
        population_script.populate_users
        population_script.populate_preference_options
        population_script.populate_matches
        population_script.assign_random_preferences

    def test_index_template_used(self):
        self.response = self.client.get(reverse_lazy('index'))
        self.content = self.response.content.decode()

        self.assertTemplateUsed(self.response, 'matches/index.html')

    def test_match_action_confirm_template_used(self):
        self.response = self.client.get(reverse('matches:match_action_confirm', kwargs={'match_id':None, 'action_type':'accepted'}))
        self.content = self.response.content.decode()

        self.assertTemplateUsed(self.response, 'matches/match_action_confirm.html')

    def test_matches_accepted_template_used(self):
        self.response = self.client.get(reverse('matches:matches_accepted'))
        self.content = self.response.content.decode()

        self.assertTemplateUsed(self.response, 'matches/matches_accepted.html')

    def test_matches_base_template_used(self):
        self.response = self.client.get(reverse('matches:matches_base'))
        self.content = self.response.content.decode()

        self.assertTemplateUsed(self.response, 'matches/matches_base.html')

    def test_matches_denied_template_used(self):
        self.response = self.client.get(reverse('matches:matches_denied'))
        self.content = self.response.content.decode()

        self.assertTemplateUsed(self.response, 'matches/matches_denied.html')

    def test_matches_pending_template_used(self):
        self.response = self.client.get(reverse('matches:matches_pending'))
        self.content = self.response.content.decode()

        self.assertTemplateUsed(self.response, 'matches/matches_pending.html')

    def test_matches_possible_template_used(self):
        self.response = self.client.get(reverse('matches:matches_possible'))
        self.content = self.response.content.decode()

        self.assertTemplateUsed(self.response, 'matches/matches_possible.html')