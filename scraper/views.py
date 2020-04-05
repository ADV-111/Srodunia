from django.shortcuts import render
from django.views import View

from scraper.scrape_club_members import get_my_club_members
from scraper.scrape_starred_segments import push_segment_to_db
from scraper.models import AthleteDetails

from scraper.strava_scraper import StravaScraper
from bs4 import BeautifulSoup


class ScrapeHomeView(View):
    def get(self, request):
        return render(request, 'scraper/scraper_home.html', context={})

    def post(self, request):
        ...


class ScrapeClubMembers(View):
    def get(self, request):
        return get_my_club_members('mirko.dravik@gmail.com', 'Dravikson123', '515628') #TODO: zrobić do tego widok, żeby wysyłać postem dane co ma zeskrpować ze stravy (lista segmentów, członków klubu, leaderboardy)

    def post(self, request):
        ...


class ScrapeSegmentsLeaderboards(View):
    def get(self, request):
        ...

    def post(self, request):
        ...


class ScrapeStarredSegments(View):
    def get(self, request):
        return push_segment_to_db()

    def post(self, request):
        ...