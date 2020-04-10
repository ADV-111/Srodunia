# Generated by Django 3.0.4 on 2020-04-09 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0004_stravasegmentleaderboard_leaderboard_unique_week_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stravasegmentleaderboard',
            name='strava_activity_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='stravasegmentleaderboard',
            name='strava_effort_id',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
