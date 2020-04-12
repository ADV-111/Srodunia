from django.urls import path

from srodunia.views import SroduniaHomeView, SegmentsAllView, WeeklyLeaderboardAllView, SegmentDetailedView, \
    SegmentEditView, AthletesAllView, AthleteDetailedView, AthleteEditView

urlpatterns = [
    path('', SroduniaHomeView.as_view(), name='home_view'),
    path('segments/', SegmentsAllView.as_view(), name='segments_all'),
    path('segments/<int:segment_id>/', SegmentDetailedView.as_view(), name='segment_detailed'),
    path('segments/<int:segment_id>/edit/', SegmentEditView.as_view(), name='segment_edit'),
    path('athletes/', AthletesAllView.as_view(), name='athletes_all'),
    path('athletes/<int:athlete_id>/', AthleteDetailedView.as_view(), name='athlete_detailed'),
    path('athletes/<int:athlete_id>/edit/', AthleteEditView.as_view(), name='athlete_edit'),
    path('leaderboards/', WeeklyLeaderboardAllView.as_view(), name='weekly_leaderboard')
]