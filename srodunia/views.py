from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django_tables2 import SingleTableView, tables
from scraper.models import StravaSegmentLeaderboard, AthleteDetails


class SroduniaHomeView(View):
    def get(self, request):
        return render(request, 'home.html', context={})


class LeaderboardTableView(ListView):
    model = AthleteDetails
    template_name = 'leaderboard.html'
    paginate_by = 10

