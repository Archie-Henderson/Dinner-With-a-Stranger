from django.urls import path
from matches import views
from .views import total_matches

app_name = 'matches'

urlpatterns = [
    path('pending/', views.matches_pending, name='matches_pending'),
    path('accepted/', views.matches_accepted, name='matches_accepted'),
    path('denied/', views.matches_denied, name='matches_denied'),
    path('possible/', views.matches_possible, name='matches_possible'),
    path('base/', views.matches_base, name='matches_base'),
    path('update/<str:match_id>/<str:status>/', views.update_match_status, name='update_match_status'),
    path('ajax/pending/', views.ajax_matches_pending, name='ajax_matches_pending'),
    path('<str:match_id>/confirm/<str:action_type>/', views.match_action_confirm, name='match_action_confirm'),
    path('api/total-matches/', total_matches, name='total-matches'),
    path('possible/accept/<int:user_id>/', views.possible_match_accept, name='possible_match_accept'),
    path('possible/deny/<int:user_id>/', views.possible_match_deny, name='possible_match_deny'),

    # path('registration/preferences/', views.registration_preferences, name='registration_preferences'),


]

#checking if I can commit 