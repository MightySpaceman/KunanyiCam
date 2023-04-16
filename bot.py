import time
from mastodon import Mastodon
import requests

def getWeather():
    weatherData = requests.get('http://reg.bom.gov.au/fwo/IDT60901/IDT60901.95979.json')
    json = weatherData.json()['observations']['data'][0]
    return json

def getImages():
    img_data = requests.get('https://hccapps.hobartcity.com.au/webcams/platform').content
    with open('platform.jpg', 'wb') as handler:
        handler.write(img_data)

    img_data = requests.get('https://hccapps.hobartcity.com.au/webcams/summit').content
    with open('summit.jpg', 'wb') as handler:
        handler.write(img_data)

def post(content, images):
    getImages()

    media_ids = []
    for image in images:
        with open(image, 'rb') as f:
            response = mastodon.media_post(f, mime_type='image/jpeg')
            media_id = response['id']
            media_ids.append(media_id)

    mastodon.status_post(content, media_ids=media_ids)

mastodon = Mastodon(
        access_token = 'TOKEN',
        api_base_url = 'https://aus.social'
    )

while True:
    data = getWeather()

    content = f"Local Conditions on Kunanyi/Mt Wellington (Last Updated {data['local_date_time']})\n\n"
    content += f"Air temperature: {data['air_temp']}°C\n"
    content += f"Apparent temperature (adjusted for wind): {data['apparent_t']}°C\n"
    content += f"Rain since 9am: {data['rain_trace']} mm\n"
    content += f"Wind speed: {data['wind_spd_kmh']}km/h\n"
    content += f"Wind gust (max) speed: {data['gust_kmh']}km/h\n"
    content += f"Wind direction: {data['wind_dir']}\n"
    content += f"\nFor road closure status visit https://hccapps.hobartcity.com.au/PinnacleRoad/\n\n"
    content += f"All image credit goes to the City of Hobart council: https://www.hobartcity.com.au/Community/kunanyi-Mt-Wellington/kunanyi-Mount-Wellington-webcams"

    post(content, {"platform.jpg", "summit.jpg"})
    time.sleep(2100)






