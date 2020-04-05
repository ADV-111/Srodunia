import requests

from scraper.get_strava_access_token import refreshed_access_token

BASE_URL = 'https://www.strava.com'
ACCESS_TOKEN = refreshed_access_token()


def get_starred_segments():
    request_dataset_url = BASE_URL + '/api/v3/segments/starred'  # check https://developers.strava.com/docs/reference/ for STRAVA API REQUESTS
    header = {'Authorization': 'Bearer ' + ACCESS_TOKEN}
    param = {'per_page': 200, 'page': 1}
    result_list = requests.get(request_dataset_url, headers=header, params=param).json()
    segments_id_list = []
    for i in result_list:
        segments_id_list.append(i['id'])
    return segments_id_list


def get_segment_details():
    starred_segment_list = get_starred_segments()
    detailed_segment_list = []
    for i in range(len(starred_segment_list)):
        request_dataset_url = BASE_URL + f'/api/v3/segments/{starred_segment_list[i]}'
        header = {'Authorization': 'Bearer ' + ACCESS_TOKEN}
        segment_details = requests.get(request_dataset_url, headers=header).json()
        detailed_segment_list.append(segment_details)
    return detailed_segment_list


if __name__ == '__main__':
    print(get_starred_segments())
    print(get_segment_details())
