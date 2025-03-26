from django.urls import path
from matches import views

app_name = 'matches'

urlpatterns = [
    path('', views.match_list, name='match_list'),
    path('<str:match_id>/', views.match_detail, name='match_detail'),

    path('pending/', views.matches_pending, name='matches_pending'),
    path('accepted/', views.matches_accepted, name='matches_accepted'),
    path('denied/', views.matches_denied, name='matches_denied'),
    path('confirmed/', views.block_confirm, name='block_confirm'),
    path('unmatch-confirmed/', views.unmatch_confirm, name='unmatch_confirm'),
]

