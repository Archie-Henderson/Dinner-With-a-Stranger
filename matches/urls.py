from django.urls import path
from matches import views

app_name = 'matches'

urlpatterns = [
    path('', views.match_list, name='match_list'),
    path('<str:match_id>/', views.match_detail, name='match_detail'),
    path('pending/', views.matches_pending, name='matches_pending'),
    path('accepted/', views.matches_accepted, name='matches_accepted'),
    path('denied/', views.matches_denied, name='matches_denied'),
    path('possible/', views.matches_possible, name='matches_possible'),
    path('block-confirm/', views.block_confirm, name='block_confirm'),
    path('unmatch-confirm/', views.unmatch_confirm, name='unmatch_confirm'),
    path('base/', views.matches_base, name='matches_base'),
    path('update/<str:match_id>/<str:decision>/', views.update_match_status, name='update_match_status'),
]
