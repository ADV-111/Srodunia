import datetime

from django.db.models import Sum, Count
from django.shortcuts import render, redirect
from django.views import View

from scraper.scrape_club_members import get_leaderboards
from scraper.models import SegmentDescription, SEGMENT_TYPES, SEGMENT_SECTIONS, SEGMENT_ZONES, SEGMENT_CATEGORIES
from scraper.models import StravaSegmentLeaderboard, AthleteDetails


class SroduniaHomeView(View):
    def get(self, request):
        return render(request, 'home.html', context={})


class SegmentsAllView(View):
    def get(self, request):
        segment_list = SegmentDescription.objects.all()
        return render(request, 'segments.html', context={'segments': segment_list})


class SegmentDetailedView(View):
    template = 'segment_detailed.html'

    def get(self, request, segment_id):
        segment = SegmentDescription.objects.get(pk=segment_id)
        this_week = int(datetime.datetime.now().isocalendar()[1])
        weeks = StravaSegmentLeaderboard.objects.all().distinct('week_number')
        leaderboard = StravaSegmentLeaderboard.objects.filter(strava_segement_id=segment_id,
                                                              week_number=this_week).order_by('rank')
        return render(request, template_name=self.template, context={'segment': segment,
                                                                     'leaderboard': leaderboard,
                                                                     'weeks': weeks,
                                                                     'week_number': this_week})

    def post(self, request, segment_id):
        segment = SegmentDescription.objects.get(pk=segment_id)
        week_number = int(request.POST.get('week_number'))
        weeks = StravaSegmentLeaderboard.objects.all().distinct('week_number')
        leaderboard = StravaSegmentLeaderboard.objects.filter(strava_segement_id=segment_id,
                                                              week_number=week_number).order_by('rank')
        return render(request, template_name=self.template, context={'segment': segment,
                                                                     'leaderboard': leaderboard,
                                                                     'weeks': weeks,
                                                                     'week_number': week_number})

class SegmentEditView(View):
    def get(self, request, segment_id):
        segment = SegmentDescription.objects.get(pk=segment_id)
        return render(request, 'segment_edit.html', context={'segment': segment,
                                                             'segment_types': SEGMENT_TYPES,
                                                             'segment_cats': SEGMENT_CATEGORIES,
                                                             'segment_zones': SEGMENT_ZONES,
                                                             'segment_sections': SEGMENT_SECTIONS}
                      )

    def post(self, request, segment_id):
        segment = SegmentDescription.objects.get(pk=segment_id)
        segment_type = request.POST.get('srodunia_segment_type')
        segment_cat = request.POST.get('srodunia_segment_cat')
        segment_zone = request.POST.get('srodunia_segment_zone')
        segment_section = request.POST.get('srodunia_segment_section')
        segment.srodunia_segment_type = segment_type
        segment.srodunia_segment_cat = segment_cat
        segment.srodunia_segment_zone = segment_zone
        segment.srodunia_segment_section = segment_section
        segment.save()
        return redirect('segments_all')


class AthletesAllView(View):
    def get(self, request):
        current_week = datetime.datetime.now().isocalendar()[1]
        a = StravaSegmentLeaderboard.objects.values()

        athletes_all = AthleteDetails.objects.all().order_by('strava_athlete_name')
        athletes = StravaSegmentLeaderboard.objects.filter(strava_athlete_id=athletes_all[1].strava_athlete_id,
                                                           week_number=current_week,
                                                           time_filter='this_week')

        return render(request, 'athletes_all.html', context={'athletes': athletes_all})

    def post(self, request):
        ...


class AthleteDetailedView(View):
    def get(self, request, athlete_id):
        athlete = AthleteDetails.objects.get(pk=athlete_id)
        results = StravaSegmentLeaderboard.objects.filter(strava_athlete_id=athlete_id, time_filter='this_week')
        return render(request, 'athlete_detailed.html', context={'athlete': athlete, 'results': results})

    def post(self, request):
        ...


class AthleteEditView(View):
    def get(self, request, athlete_id):
        athlete = AthleteDetails.objects.get(pk=athlete_id)
        return render(request, 'athlete_edit.html', context={'athlete': athlete})

    def post(self, request):
        ...


class WeeklyLeaderboardAllView(View):
    def get(self, request):
        this_week = int(datetime.datetime.now().isocalendar()[1])
        weeks = StravaSegmentLeaderboard.objects.all().distinct('week_number')
        # leaderboard = StravaSegmentLeaderboard.objects.filter(week_number=0, time_filter='this_week', strava_segement_id=34).values('strava_athlete_id__strava_athlete_name').annotate(sum_points=Sum('points'), effort_count=Count('strava_effort_id'))
        leaderboard = StravaSegmentLeaderboard.objects.filter(time_filter='this_week').values('strava_athlete_id__strava_athlete_name', 'strava_athlete_id').annotate(sum_points=Sum('points'), effort_count=Count('strava_effort_id'))
        return render(request, 'leaderboard.html', context={'leaderboard': leaderboard})

    def post(self, request):
        ...


class TestView(View):
    def get(self, request):
        get_leaderboards('mirko.dravik@gmail.com', 'Dravikson123')
        return render(request, 'test.html', {})
