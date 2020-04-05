from django.urls import path

from scraper.views import ScrapeClubMembers, ScrapeStarredSegments

urlpatterns = [
    path('scrape/members/', ScrapeClubMembers.as_view()),
    path('scrape/segments/', ScrapeStarredSegments.as_view()),
]