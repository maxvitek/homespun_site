import homespun_site.settings as settings
import requests
import json
import datetime


class Service(object):
    '''
    abstraction of cloud services used to store data
    '''
    def __init__(self):
        pass

    def get_data(self):
        raise MustOverrideMethod()

class MustOverrideMethod(Exception):
    pass


class Flower(Service):
    '''
    Parrot Flower Power
    '''
    CLIENT_ID = settings.FLOWER_CLIENT_ID
    CLIENT_SECRET = settings.FLOWER_CLIENT_SECRET
    USERNAME = settings.FLOWER_USERNAME
    PASSWORD = settings.FLOWER_PASSWORD
    BASE_URL = "https://apiflowerpower.parrot.com"

    def __init__(self):
        resource = "/user/v1/authenticate"
        payload = {
                    'grant_type': 'password',
                    'client_id': self.CLIENT_ID,
                    'client_secret': self.CLIENT_SECRET,
                    'username': self.USERNAME,
                    'password': self.PASSWORD,
                  }
        headers = {
                'Accept-Language': 'en_us',
                }
        url = self.BASE_URL + resource
        r = requests.post(url, data=payload, headers=headers)
        r_dict = json.loads(r.content)

        self.access_token = r_dict['access_token']
        self.oauth_bearer = { 'Authorization':'Bearer ' + self.access_token }
        
        location_resource = "/sensor_data/v2/sync?include_s3_urls=1"
        payload = { 'include_s3_urls': '1' }
        url = self.BASE_URL + location_resource
        r = requests.get(url, params=payload, headers=self.oauth_bearer)
        r_dict = json.loads(r.content)

        # This is hacked to use only the first location!  It's because I only have ONE!
        self.location_id = r_dict['locations'][0]['location_identifier']
        self.last_sample_date = datetime.datetime.strptime(r_dict['locations'][0]['last_sample_utc'], '%Y-%m-%d %H:%M:%S UTC')

    def get_data(self, days):
        from_datetime = (self.last_sample_date - datetime.timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S UTC')
        to_datetime = self.last_sample_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        resource = '/sensor_data/v2/sample/location/' + self.location_id + '?from_datetime_utc=' + from_datetime + '&to_datetime_utc=' + to_datetime
        url = self.BASE_URL + resource

        r = requests.get(url, headers=self.oauth_bearer)
        
        raw_data = json.loads(r.content)['samples']
        data = []
        for d in raw_data:
            data.append({
                'plant_temp': float(d['air_temperature_celsius']) * 9 / 5 + 32,
                'sunlight': float(d['par_umole_m2s']),
                'water': float(d['vwc_percent']),
                'datetime': datetime.datetime.strptime(d['capture_ts'], '%Y-%m-%dT%H:%M:%SZ'),
                })
        return data
