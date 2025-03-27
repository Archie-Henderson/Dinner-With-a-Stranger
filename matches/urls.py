from django.urls import path
from matches import views

app_name = 'matches'

urlpatterns = [
    path('pending/', views.matches_pending, name='matches_pending'),
    path('accepted/', views.matches_accepted, name='matches_accepted'),
    path('denied/', views.matches_denied, name='matches_denied'),
    path('possible/', views.matches_possible, name='matches_possible'),
    path('base/', views.matches_base, name='matches_base'),
    path('update/<str:match_id>/<str:decision>/', views.update_match_status, name='update_match_status'),
    path('ajax/pending/', views.ajax_matches_pending, name='ajax_matches_pending'),
    path('<str:match_id>/confirm/<str:action_type>/', views.match_action_confirm, name='match_action_confirm'),

]
