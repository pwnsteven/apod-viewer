import requests
import traceback

from django.conf import settings

from outside.nasa.models import Apod


def get_acceptable_resp_status_codes():
    return [200]


def get_api(date, api_key=None):
    """ instantiate util for prod key """

    if api_key:
        return API(date, api_key)
    return API(date, settings.NASA_API_SECRET)


class API:
    """ The APOD API class. Provides basic http request functionality for the NASA APOD API """

    def __init__(self, date, api_key=None):
        """
        Arguments:
            date: the date of the requested APOD (format: YYYY-MM-DD)
            api_key: an api key to override the default / demo key
        """
        self.apod_url = 'https://api.nasa.gov/planetary/apod'

        self.api_key = 'DEMO_KEY'
        if api_key:
            self.api_key = api_key

        self.date = date
        self.session = requests.Session()

    def get_apod_params(self):
        """ Build parameters
        """
        params = {
            'api_key': self.api_key,
            'date': self.date
        }
        return params

    def get_apod(self):
        """Returns the JSON payload from the apod url.

        Refs:
        - NASA API Documentation: https://api.nasa.gov/
        - Requests Documentation: https://requests.readthedocs.io/en/master/user/quickstart/
        """
        params = self.get_apod_params()
        apod_response = self.session.get(self.apod_url, params=params)
        status_code = apod_response.status_code
        if status_code in get_acceptable_resp_status_codes():
            return True, apod_response.json()

        msg = ''
        if status_code in range(400, 500):
            stack = traceback.format_exc()
            msg = f'oops, lets see what went wrong:\n\n{stack}'

        if status_code in range(500, 600):
            msg = f"c'mon nasa... "

        # Handle failed response from calling processes...
        return False, f'Invalid APOD API Response. HTTP [{status_code}] {msg}'
