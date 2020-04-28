from scraper.models import SegmentDescription
from scraper.request_dataset_through_api import get_segment_details


def push_segment_to_db():
    print('Updating Segment Data Base')
    segments_list = get_segment_details()
    for i in segments_list:
        segment_id = i['id']
        SegmentDescription.objects.update_or_create(
            strava_segment_id=segment_id,
            defaults=dict(strava_segment_name=i['name'],
                          distance=i['distance'],
                          average_grade=i['average_grade'],
                          maximum_grade=i['maximum_grade'],
                          start_latitude=i['start_latitude'],
                          start_longitude=i['start_longitude'],
                          end_latitude=i['end_latitude'],
                          end_longitude=i['end_longitude'],
                          climb_category=i['climb_category'],
                          total_elevation_gain=i['total_elevation_gain'],
                          strava_effort_count=i['effort_count'],
                          star_count=i['star_count'])
        )


if __name__ == '__main__':
    push_segment_to_db()
