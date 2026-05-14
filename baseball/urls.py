from django.urls import path
from .views import (
    TeamQuestionListView,
    PlayerQuestionListView,
    TeamListView,
    TeamDetailView,
    TeamPlayerListView,
    PlayerDetailView,
    TeamRecommendView,
    PlayerRecommendView,
)

urlpatterns = [
    path('questions/team/', TeamQuestionListView.as_view()),
    path('questions/player/', PlayerQuestionListView.as_view()),
    path('recommend/team/', TeamRecommendView.as_view()),
    path('recommend/player/', PlayerRecommendView.as_view()),
    path('teams/', TeamListView.as_view()),
    path('teams/<int:pk>/', TeamDetailView.as_view()),
    path('teams/<int:pk>/players/', TeamPlayerListView.as_view()),
    path('players/<int:pk>/', PlayerDetailView.as_view()),
]
