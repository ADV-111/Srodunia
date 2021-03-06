from django.urls import path

from scraper.views import ScrapeClubMembers, ScrapeStarredSegments, ScrapeHomeView, ScrapeSegmentsLeaderboards

urlpatterns = [
    path('scrape/', ScrapeHomeView.as_view(), name='scrape_home'),
    path('scrape/leaderboards/', ScrapeSegmentsLeaderboards.as_view(), name='scrape_leaderboards'),
    path('scrape/members/', ScrapeClubMembers.as_view(), name='scrape_members'),
    path('scrape/segments/', ScrapeStarredSegments.as_view(), name='scrape_segments'),
]