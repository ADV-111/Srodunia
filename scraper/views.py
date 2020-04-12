from django.shortcuts import render
from django.views import View

from scraper.scrape_club_members import get_my_club_members
from scraper.scrape_starred_segments import push_segment_to_db
from scraper.scrape_leaderboards import scrape_weekly_leaderboards
from scraper.models import AthleteDetails, SegmentDescription, StravaSegmentLeaderboard

from scraper.strava_scraper import StravaScraper
from bs4 import BeautifulSoup


class ScrapeHomeView(View):
    def get(self, request):
        return render(request, 'scraper/scraper_home.html', context={})

    def post(self, request):
        ...


class ScrapeClubMembers(View):
    def get(self, request):
        athletes = AthleteDetails.objects.all()
        return render(request, 'scraper/scrape_members.html', context={'athletes': athletes})

    def post(self, request):
        get_my_club_members('mirko.dravik@gmail.com', 'Dravikson123',
                            '515628')  # TODO: zrobić do tego widok, żeby wysyłać postem dane co ma zeskrpować ze stravy (lista segmentów, członków klubu, leaderboardy)
        return self.get(request)


class ScrapeSegmentsLeaderboards(View):
    def get(self, request):
        segments_to_scrape = SegmentDescription.objects.all()
        return render(request, 'scraper/scrape_leaderboards.html', context={'segments': segments_to_scrape})

    def post(self, request):
        segments_to_scrape = request.POST.getlist('strava_segment_id')
        print(segments_to_scrape)
        scrape_weekly_leaderboards('mirko.dravik@gmail.com', 'Dravikson123', segments_to_scrape, 'This Week')
        return self.get(request)


class ScrapeStarredSegments(View):
    def get(self, request):
        segments = SegmentDescription.objects.all()
        return render(request, 'scraper/scrape_segments.html', context={'segments': segments})

    def post(self, request):
        push_segment_to_db()
        return self.get(request)
