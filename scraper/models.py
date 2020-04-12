from django.db import models

SEGMENT_TYPES = (
    ('1', '1 - 4 minuty'),
    ('5', '5 - 15 minut'),
    ('20', '16 - 44 minut'),
    ('60', '45 - 110 minut'),
    ('110', 'powyżej 110 minut'),
)
SEGMENT_CATEGORIES = (
    ('-1', 'DH: < 0%'),
    ('0', 'FLAT: 0 - 4%'),
    ('1', 'ROLL: 4 - 8%'),
    ('2', 'HILL: 8 - 12%'),
    ('3', 'CLIMB: > 12%'),
)
SEGMENT_ZONES = (
    ('5', 'MAX 5 Pkt'),
    ('6', 'MAX 6 Pkt'),
    ('7', 'MAX 7 Pkt'),
)
SEGMENT_SECTIONS = (
    ('NW', '↖️ PN-ZACH'),
    ('NE', 'PN-WSCH ↗️'),
    ('SW', '↙️ PD-ZACH'),
    ('SE', 'PD-WSCH ↘️'),
)


class SegmentDescription(models.Model):
    strava_segment_id = models.IntegerField(unique=True)
    strava_segment_name = models.CharField(max_length=255)
    distance = models.FloatField(null=True)
    average_grade = models.FloatField(null=True) #TODO: bardziej wiarygodne dane odnośnie max gradient znajdują się na veloviewer
    maximum_grade = models.FloatField(null=True) #TODO: własne miara czy segment jest płaski, pofałdowany, górka, czy sztfajfa (elev.gain / dystnas)
    start_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    start_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    end_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    end_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    climb_category = models.IntegerField(null=True)
    total_elevation_gain = models.FloatField(null=True)
    strava_effort_count = models.IntegerField(null=True)
    star_count = models.IntegerField(null=True)
    srodunia_segment_type = models.CharField(choices=SEGMENT_TYPES, null=True, max_length=255)
    srodunia_segment_cat = models.CharField(choices=SEGMENT_CATEGORIES, null=True, max_length=255)
    srodunia_segment_zone = models.CharField(choices=SEGMENT_ZONES, null=True, max_length=255)
    srodunia_segment_section = models.CharField(choices=SEGMENT_SECTIONS, null=True, max_length=255)
    date_added = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.strava_segment_name}'


class StravaClubs(models.Model):
    club_id = models.IntegerField(unique=True)
    club_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.club_name}'


class AthleteDetails(models.Model):
    strava_athlete_id = models.IntegerField(unique=True)
    strava_athlete_name = models.CharField(max_length=255)
    srodunia_athlete_name = models.CharField(max_length=255, null=True)
    athlete_avatar_img_url = models.URLField()
    role = models.CharField(max_length=32)
    club_id = models.ManyToManyField(StravaClubs)
    date_added = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.strava_athlete_name}'


class StravaSegmentLeaderboard(models.Model):
    leaderboard_unique_week_number = models.CharField(max_length=255, null=True)
    rank = models.IntegerField() #TODO: jest możliwość zeskrobania KOMa dla segmentu
    strava_athlete_id = models.ForeignKey(AthleteDetails, on_delete=models.CASCADE, null=True)
    strava_activity_id = models.CharField(max_length=255)
    strava_effort_id = models.CharField(max_length=255, unique=True)
    strava_segement_id = models.ForeignKey(SegmentDescription, on_delete=models.CASCADE, null=True)
    effort_date = models.DateField()
    avg_speed = models.CharField(max_length=32)
    avg_hr = models.CharField(max_length=32, null=True)
    avg_power = models.CharField(max_length=32, null=True)
    vam = models.CharField(max_length=32, null=True)
    time_result = models.CharField(max_length=10)
    time_filter = models.CharField(max_length=32, null=True)
    club_id = models.ForeignKey(StravaClubs, on_delete=models.CASCADE, null=True)
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    points = models.IntegerField(null=True)
    week_number = models.IntegerField(null=True)
