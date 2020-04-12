from scraper.models import AthleteDetails, StravaClubs

from scraper.strava_scraper import StravaScraper
from bs4 import BeautifulSoup


def push_athlete_to_db(strava_athlete_id, strava_athlete_name, athlete_avatar_img_url, role, strava_club_id):
    athlete, created = AthleteDetails.objects.get_or_create(
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


if __name__ == '__main__':
    get_my_club_members('mirko.dravik@gmail.com', 'Dravikson123', '515628')
