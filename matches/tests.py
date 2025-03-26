import os
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from django.test.client import Client
from django.contrib.auth.models import User

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

        self.pages={'match_list':('',self.views_module.match_list),'match_detail':('10/',self.views_module.match_detail), 'matches_pending':('pending/',self.views_module.matches_pending), 'matches_accepted':('accepted/',self.views_module.matches_accepted),'matches_denied':('denied/',self.views_module.matches_denied), 'matches_possible':('possible/',self.views_module.matches_possible), 'block_confirm':('block-confirm/',self.views_module.block_confirm), 'unmatch_confirm':('unmatch/',self.views_module.unmatch_confirm), 'matches_base':('base/',self.views_module.matches_base), 'update_match_status':('update/10/y/',self.views_module.update_match_status)}

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