from django.apps import AppConfig


class UserPageConfig(AppConfig):
    name = 'user_page'

    def ready(self):
        import user_page.signals  # Import the signals module

