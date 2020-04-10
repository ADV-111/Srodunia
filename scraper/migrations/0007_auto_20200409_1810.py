# Generated by Django 3.0.4 on 2020-04-09 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0006_auto_20200409_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stravasegmentleaderboard',
            name='strava_athlete_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scraper.AthleteDetails'),
        ),
        migrations.AlterField(
            model_name='stravasegmentleaderboard',
            name='strava_segement_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scraper.SegmentDescription'),
        ),
    ]