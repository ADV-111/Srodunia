from scraper.models import AthleteDetails, StravaClubs

from scraper.strava_scraper import StravaScraper
from bs4 import BeautifulSoup
import requests


def push_athlete_to_db(strava_athlete_id, strava_athlete_name, athlete_avatar_img_url, role, strava_club_id):
    athlete, created = AthleteDetails.objects.update_or_create(
        strava_athlete_id=strava_athlete_id,
        defaults=dict(strava_athlete_id=strava_athlete_id, strava_athlete_name=strava_athlete_name,
                      athlete_avatar_img_url=athlete_avatar_img_url, role=role)
    )
    club_pk = StravaClubs.objects.get(club_id=strava_club_id)
    athlete.club_id.add(club_pk)


def get_my_club_members(email: str, password: str, strava_club_id: str):
    email = email
    password = password
    scraper = StravaScraper(email, password)
    scraper.login()
    print('Logged in to STRAVA')

    page = 1
    while page < 100:
        try:
            print(f'Scrapping page: {page}')
            url = f"https://www.strava.com/clubs/{strava_club_id}/members?page={page}"
            response = scraper.get_page(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            if page > 1:
                pass
            else:
                admins = soup.findAll('ul', {'class': 'list-athletes'})[0].findAll('div', {'class': 'avatar'})
                for i in admins:
                    strava_athlete_name = i.get('title').strip()
                    strava_athlete_id = i.find('a').get('href').split(sep='/')[-1]
                    athlete_avatar_img_url = i.find('img').get('src')
                    role = 'admin'
                    push_athlete_to_db(strava_athlete_id, strava_athlete_name, athlete_avatar_img_url, role,
                                       strava_club_id)
                    print(strava_athlete_name, strava_athlete_id, role, athlete_avatar_img_url)

            members = soup.findAll('ul', {'class': 'list-athletes'})[1].findAll('div', {'class': 'avatar'})
            for i in members:
                strava_athlete_name = i.get('title').strip()
                strava_athlete_id = i.find('a').get('href').split(sep='/')[-1]
                athlete_avatar_img_url = i.find('img').get('src')
                role = 'member'
                push_athlete_to_db(strava_athlete_id, strava_athlete_name, athlete_avatar_img_url, role,
                                   strava_club_id)
                print(strava_athlete_name, strava_athlete_id, role, athlete_avatar_img_url)
            page += 1
        except IndexError as err:
            print(err)
            break


def get_leaderboards(email, password):
    # email = email
    # password = password
    # scraper = StravaScraper(email, password)
    # scraper.login()
    # print('Logged in to STRAVA')
    # url = f"https://www.strava.com/dashboard"
    # response = scraper.get_page(url)
    # cookie = response.request.headers["Cookie"]

    import requests

    url = "https://www.strava.com/segments/23332840/leaderboard?age_group=35_44&club_id=515628&date_range=this_week&filter=club&weight_class=0_54&partial=true"

    payload = {}
    headers = {
        'authority': 'www.strava.com',
        'accept': 'text/html, */*; q=0.01',
        'x-csrf-token': 'vT/Hs6pCt7OMgSGPsGb9vlCGl7tqYBDtZaDE4oV9oVpJwjPo98bSWw1yzrLogBcWqlAIEV+DQdJb8h8Aif4ZCQ==',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.strava.com/segments/23332840',
        'accept-language': 'pl,pl-PL;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6,it;q=0.5',
        'cookie': 'sp=4ce32d78-3dd5-4922-b502-babad94666d9; _ga=GA1.2.1261343235.1587245251; _gid=GA1.2.1964747499.1587245251; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; _strava_cookie_banner=true; _strava4_session=5o5o647so9dh68jop7u9drrfa3o1qd0k; ajs_user_id=52749464; ajs_anonymous_id=%22ea6e070e-1fa7-4562-b0a3-467dab19b0b2%22; elevate_daily_connection_done=true; elevate_athlete_update_done=true; ajs_group_id=null; explore_activity_type=cycling; _sp_ses.047d=*; _sp_id.047d=87a25187-f2ff-433a-ab38-f674ec087f4c.1587245276.2.1587249422.1587245857.e5539f92-ad61-415c-8945-42ea3cf77368',
        'Cookie': 'SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; elevate_daily_connection_done=true; _strava4_session=12g1lk4gjmliuaa11t50fuerd3vbtsq1; elevate_athlete_update_done=true; explore_activity_type=cycling; _sp_id.047d=87a25187-f2ff-433a-ab38-f674ec087f4c.1587245276.1.1587245857..238f5e0f-524a-42b2-a66e-a4d8283c96f7'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text.encode('utf8'))

    # # response_1 = scraper.get_page(url_1)
    # print(cookie)
    # soup = BeautifulSoup(res.content, 'html.parser')
    # print(soup)


if __name__ == '__main__':
    get_my_club_members('mirko.dravik@gmail.com', 'Dravikson123', '515628')
