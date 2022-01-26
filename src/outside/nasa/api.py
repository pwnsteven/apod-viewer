from django.conf import settings
import requests


def get_api():
    return API(settings.NASA_API_SECRET)


class API:
    def __init__(self, api_key):
        self.api_key = api_key
        self.apod_url = 'https://api.nasa.gov/planetary/apod'

    def get_apod(self):
        """Returns the JSON payload from the apod url.

        NASA API Documentation: https://api.nasa.gov/
        Requests Documentation: https://requests.readthedocs.io/en/master/user/quickstart/
        """
        # Use the `requests` library to call the API with the correct parameters and return the
        # JSON response.
        pass
