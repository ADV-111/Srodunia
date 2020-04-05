import json
import csv
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome("./bin/chromedriver", options=chrome_options)


def login():
    driver.get("https://www.strava.com/login")
    email = "mirko.dravik@gmail.com"
    password = "Dravikson123"

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
    print(f'Selected segment no. {segment_id}')


def team_filter_selection(clubid='515628'):
    club_id = driver.find_element_by_css_selector(f'[data-clubid="{clubid}"]')
    club_id.click()
    print(f'Team filter applied: EWODD RACE TEAM.')
    print('Selecting time-frame...')
    time.sleep(1)


def time_frame_selection(time_frame='This Month'):  # ['Today', 'This Week', 'This Month', This Year']
    # Selecting Time Frame for the table
    time_frame_btn = driver.find_element_by_xpath('//*[@id="segment-results"]/div[2]/table/tbody/tr/td[3]/div/button')
    time_frame_btn.click()
    time.sleep(1)
    if time_frame == 'This Year':
        select_time_frame = driver.find_elements_by_link_text(time_frame)[1]
    else:
        select_time_frame = driver.find_element_by_link_text(time_frame)
    select_time_frame.click()
    print(f'Time frame selected: {time_frame}. Printing html...')
    time.sleep(2)


def get_and_print_html():
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
                # effort_properties = row_properties[2]
                # effort_properties = row.find_all('td', {'class': 'track-click'})[1]
                athlete_properties = row.find('td', {'class': 'athlete track-click'})
                data_tracking = json.loads(athlete_properties.attrs.get('data-tracking-properties'))
                rank = data_tracking.get('rank')
                athlete_id = data_tracking.get('athlete_id')
                activity_id = data_tracking.get('activity_id')
                segment_effort_id = data_tracking.get('segment_effort_id')
                athlete_full_name = athlete_properties.find('a').text.strip()
                athlete_abbr_name = ...
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
                    [f'{rank},{athlete_full_name},{athlete_id},{activity_id},{segment_effort_id},{date},{speed},{hr},{power},{vam},{time_result},{club_id}'])
    except AttributeError as err:
        print(f"There's no data to fetch - AttributeError: {err}")


if __name__ == '__main__':
    login()
    segment_selection('23067094')
    team_filter_selection()
    time_frame_selection('Today')
    get_and_print_html()
