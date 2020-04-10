from django.urls import path

from srodunia.views import SroduniaHomeView, LeaderboardTableView

urlpatterns = [
    path('', SroduniaHomeView.as_view(), name='home_view'),
    path('leaderboards/', LeaderboardTableView.as_view(), name='leaderboards')
]