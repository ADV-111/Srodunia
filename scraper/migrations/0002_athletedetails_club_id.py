# Generated by Django 3.0.4 on 2020-04-03 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='athletedetails',
            name='club_id',
            field=models.ManyToManyField(to='scraper.StravaClubs'),
        ),
    ]