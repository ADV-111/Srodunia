import json
import csv
import time
import datetime

from scraper.models import StravaSegmentLeaderboard, AthleteDetails, SegmentDescription, StravaClubs

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome("scraper/bin/chromedriver", options=chrome_options)


def login(strava_login_email, strava_password):
    driver.get("https://www.strava.com/login")
    email = strava_login_email
    password = strava_password

    email_element = driver.find_element_by_id('email')
    password_element = driver.find_element_by_id('password')
    login_button = driver.find_element_by_id('login-button')
    email_element.send_keys(email)
    password_element.send_keys(password)
    login_button.click()
    print('User has logged in. Going to segment selection...')
    time.sleep(1)


def segment_selection(segment_id):
    driver.get(f'https://www.strava.com/segments/{segment_id}')
    time.sleep(2)
    print(f'Selected segment no. {segment_id}')


def team_filter_selection(clubid='515628'):
    club_id = driver.find_element_by_css_selector(f'[data-clubid="{clubid}"]')
    club_id.click()
    print(f'Team filter applied: EWODD RACE TEAM.')
    print('Selecting time-frame...')
    time.sleep(2)


def time_frame_selection(time_frame='This Week'):  # ['Today', 'This Week', 'This Month', This Year']
    # Selecting Time Frame for the table
    time_frame_btn = driver.find_element_by_xpath('//*[@id="segment-results"]/div[2]/table/tbody/tr/td[3]/div/button')
    time_frame_btn.click()
    time.sleep(1)
    if time_frame == 'This Year':
        select_time_frame = driver.find_elements_by_link_text(time_frame)[1]
    else:
        select_time_frame = driver.find_element_by_link_text(time_frame)
    select_time_frame.click()
    print(f'Time frame selected: {time_frame}. Fetching Leaderboard')
    time.sleep(5)


def ewodd_weekly_segment_selection(segment_id, time_frame):
    segment_selection(segment_id)
    team_filter_selection()
    time_frame_selection(time_frame)


def get_and_save_to_csv():
    html = driver.execute_script('return document.documentElement.outerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    clubid = json.loads(soup.find('div', {'class': 'leaderboard'}).attrs.get('data-tracking')).get(
        'leaderboard_state')  # .get('club_id')
    results_table = soup.find('table', {'class': 'table-leaderboard'}).find('tbody')
    rows = results_table.findAllNext('tr')
    file_path = './bin/20200401_IC_NS.csv'
    try:
        with open(file_path, 'a', newline='') as textfile:
            for row in rows:
                row_properties = row.find_all('td')
                athlete_properties = row.find('td', {'class': 'athlete track-click'})
                data_tracking = json.loads(athlete_properties.attrs.get('data-tracking-properties'))
                rank = data_tracking.get('rank')
                athlete_id = data_tracking.get('athlete_id')
                activity_id = data_tracking.get('activity_id')
                segment_effort_id = data_tracking.get('segment_effort_id')
                athlete_full_name = athlete_properties.find('a').text.strip()
                date = row_properties[2].text.strip()
                speed = row_properties[3].text.strip()
                hr = row_properties[4].text.strip()
                power = row_properties[5].text.strip()
                vam = row_properties[6].text.strip()
                time_result = row_properties[7].text.strip()
                club_id = clubid
                print(rank, "---", athlete_full_name, "---", date, "---", speed, "---", hr, "---", power, "---", vam,
                      "---", time_result, "---", club_id)
                writer = csv.writer(textfile)
                writer.writerow(
                    [
                        f'{rank},{athlete_full_name},{athlete_id},{activity_id},{segment_effort_id},{date},{speed},{hr},{power},{vam},{time_result},{club_id}'])
    except AttributeError as err:
        print(f"There's no data to fetch - AttributeError: {err}")


def push_leaderboard_to_db(leaderboard_athlete_number, defaults, foreign_keys):
    leaderboard, created = StravaSegmentLeaderboard.objects.update_or_create(
        leaderboard_unique_week_number=leaderboard_athlete_number,
        defaults=defaults)
    athlete_id = AthleteDetails.objects.get(strava_athlete_id=foreign_keys.get('strava_athlete_id'))
    segment_id = SegmentDescription.objects.get(strava_segment_id=foreign_keys.get('strava_segement_id'))
    club_id = StravaClubs.objects.get(club_id=foreign_keys.get('club_id'))
    leaderboard.strava_athlete_id = athlete_id
    leaderboard.strava_segement_id = segment_id
    leaderboard.club_id = club_id
    leaderboard.save()


def get_leaderboard(segment_id):
    html = driver.execute_script('return document.documentElement.outerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    leaderboard_state = json.loads(soup.find('div', {'class': 'leaderboard'}).attrs.get('data-tracking')).get(
        'leaderboard_state')#.get('club_id')
    results_table = soup.find('table', {'class': 'table-leaderboard'}).find('tbody')
    rows = results_table.findAllNext('tr')
    now = datetime.datetime.now()
    time_filter = leaderboard_state.get('time_filter')
    try:
        for row in rows:
            row_properties = row.find_all('td')
            athlete_properties = row.find('td', {'class': 'athlete track-click'})
            data_tracking = json.loads(athlete_properties.attrs.get('data-tracking-properties'))
            if time_filter == 'today':
                leaderboard_athlete_number = str(now.isocalendar()[0]) + \
                                         str(now.isocalendar()[1]) + \
                                         str(segment_id) + \
                                         str(data_tracking.get('athlete_id')) + 'TODAY'
            else:
                leaderboard_athlete_number = str(now.isocalendar()[0]) + \
                                             str(now.isocalendar()[1]) + \
                                             str(segment_id) + \
                                             str(data_tracking.get('athlete_id'))
            defaults = dict(
                leaderboard_unique_week_number=leaderboard_athlete_number,
                rank=data_tracking.get('rank'),
                strava_activity_id=str(data_tracking.get('activity_id')),
                strava_effort_id=str(data_tracking.get('segment_effort_id')),
                # athlete_full_name = athlete_properties.find('a').text.strip(),
                effort_date=datetime.datetime.strptime(row_properties[2].text.strip(), '%b %d, %Y'),
                avg_speed=row_properties[3].text.strip(),
                avg_hr=row_properties[4].text.strip(),
                avg_power=row_properties[5].text.strip(),
                vam=row_properties[6].text.strip(),
                time_result=row_properties[7].text.strip(),
                time_filter=time_filter
                # TODO: czy da się to od razu sformatować na czas: HH:MM:SS jeżeli dane są czasami przesyłane jako HH:MM:SS a czasem MM:SS
            )
            foreign_keys = dict(
                strava_athlete_id=int(data_tracking.get('athlete_id')),
                strava_segement_id=int(segment_id),
                club_id=int(leaderboard_state.get('club_id'))
            )
            push_leaderboard_to_db(leaderboard_athlete_number, defaults, foreign_keys)
    except AttributeError as err:
        print(f"There's no data to fetch - AttributeError: {err}")


def scrape_weekly_leaderboards(email, password, segments: list, time_frame):
    login(email, password)
    for segment in segments:
        ewodd_weekly_segment_selection(segment, time_frame)
        get_leaderboard(segment)


if __name__ == '__main__':
    login()
    segment_selection('23067094')
    team_filter_selection()
    time_frame_selection('Today')
