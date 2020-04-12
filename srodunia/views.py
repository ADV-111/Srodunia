import datetime

from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views import View
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
                                                                     'weeks': weeks})


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
        athletes = StravaSegmentLeaderboard.objects.all()
        return render(request, 'athletes_all.html', context={'athletes': athletes})

    def post(self, request):
        ...


class AthleteDetailedView(View):
    def get(self, request, athlete_id):
        athlete = AthleteDetails.objects.get(pk=athlete_id)
        return render(request, 'athlete_detailed.html', context={'athlete': athlete})


    def post(self, request):
        ...


class AthleteEditView(View):
    def get(self, request):
        athlete = AthleteDetails.objects.get(pk=athlete_id)
        return render(request, 'athlete_edit.html', context={'athlete': athlete})

    def post(self, request):
        ...


class WeeklyLeaderboardAllView(View):
    def get(self, request):
        leaderboard = StravaSegmentLeaderboard.objects.all().values('strava_athlete_id__strava_athlete_name').annotate(Sum('points'))
        return render(request, 'leaderboard.html', context={'leaderboard': leaderboard})

    def post(self, request):
        ...
