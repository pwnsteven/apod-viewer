import json
import requests

from django import test
from django.test import SimpleTestCase
from unittest import mock
from requests.models import Response

from outside.nasa import api as nasa_api
from outside.nasa import views as nasa_views
from outside.nasa import forms as nasa_forms


def mocked_requests_get(date, **kwargs):

    response = Response()
    response_content = None

    request_key = kwargs['params'].get('api_key', None)
    request_date = date

    if request_key == 'invalid_key':
        response.status_code = 500
        response_content = json.dumps(f'Invalid APOD API Response [{response.status_code}]')

    elif request_key == 'valid_key':
        response.status_code = 200
        response_data = {
           "date": "2022-01-27",
            "title": "foobar"
        }
        response_content = json.dumps(response_data)

    response._content = str.encode(response_content)

    return response


class ApodApiTest(test.TestCase):

    @mock.patch('requests.Session.get', side_effect=mocked_requests_get)
    def test_apod_api(self, get_mock):

        # Unsuccessful APOD call:
        apod_api = nasa_api.get_api('2022-01-27', 'invalid_key')
        resp = apod_api.get_apod()
        self.assertEqual(resp[0], False)
        self.assertEqual(resp[1], "Invalid APOD API Response. HTTP [500] c'mon nasa... ")

        # Successful APOD call:
        apod_api = nasa_api.get_api('2022-01-27', 'valid_key')
        resp = apod_api.get_apod()
        self.assertEqual(resp[0], True)
        self.assertEqual(type(resp[1]), dict)


class ApodFormTest(SimpleTestCase):

    def test_date_form(self):
        """ Test the form validation """

        form = nasa_forms.ApodSearchForm(data={
            'apod_date': '2022-01-27'
        })
        self.assertEqual(form.is_valid(), True)

        form = nasa_forms.ApodSearchForm(data={
            'apod_date': '01-27-2022'
        })
        self.assertEqual(form.is_valid(), False)
