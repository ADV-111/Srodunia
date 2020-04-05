import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = 'https://www.strava.com'


def refreshed_access_token():
    auth_url = BASE_URL + '/oauth/token'

    payload = {
        'client_id': '45452',
        'client_secret': 'a4f90933ed58bb2e081229fc97165aeac4befa74',
        'refresh_token': '970fb40553628fd4c35aa2dcf5a69b92653550e7',
        'grant_type': 'refresh_token',
        'f': 'json'
    }
    access_token = requests.post(auth_url, data=payload, verify=False).json()['access_token']
    return access_token


if __name__ == '__main__':
    refreshed_access_token()
