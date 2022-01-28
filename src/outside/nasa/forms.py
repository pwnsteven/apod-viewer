import datetime

from django import forms

from .utils import valid_date


class ApodSearchForm(forms.Form):
    """ For search form across UI header """

    apod_date = forms.CharField(required=False)

    # Provide form / date validations below...
    def clean_apod_date(self):
        """ Verify correct date format

        returns: two-tuple. boolean indicating status and the data
        """
        apod_date = self.cleaned_data.get('apod_date', '')

        if not valid_date(apod_date):
            raise forms.ValidationError(f'Invalid date format - {apod_date}.')
        return apod_date


