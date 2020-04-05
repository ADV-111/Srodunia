from django.db import models


class StravaSummaryClub(models.Model):
    strava_club_id = models.IntegerField()
    club_name = models.CharField(max_length=128)
    profile_photo_md = models.URLField(null=True)
    profile_photo = models.URLField(null=True)
    club_url = models.URLField(null=True)


class StravaDetailedAthlete(models.Model):
    strava_id = models.IntegerField()
    username = models.CharField(max_length=128)
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    profile_photo_md = models.URLField(null=True)
    profile_photo = models.URLField(null=True)
    sex = models.CharField(choices=(('M', 'M'), ('F', 'F')), max_length=1)
    strava_summit = models.BooleanField(default=False)
    ftp = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    clubs = models.ManyToManyField(StravaSummaryClub)


class AthleteProfile(models.Model):
    strava_profile = models.OneToOneField(StravaDetailedAthlete, on_delete= models.CASCADE)
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)



