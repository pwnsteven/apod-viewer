import datetime

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from .api import get_api
from .forms import ApodSearchForm
from .models import Apod
from .utils import valid_date

TODAY = datetime.date.today().strftime('%Y-%m-%d')


# ==================================================
# Views
# --------------------------------------------------
def homepage(request):
    """Render the homepage.
    """
    template = 'homepage.html'
    ctx = {'today': TODAY}

    return render(request, template, ctx)


def search(request):
    """ A view for the search results. Just a quick validation and a redirect """

    response_data = dict(request.GET)
    apod_date = response_data['apod_date'][0]

    # validate the user input
    search_form = ApodSearchForm(request.GET or None)
    valid_form = search_form.is_valid()
    if valid_form:
        return redirect(f'/apod/{apod_date}')
    else:
        messages.error(request, f'Invalid date provided ({apod_date}). Please use format YYYY-MM-DD and try again')
        return redirect(f'/apod/{TODAY}')


def apod(request, **kwargs):
    """ A view that renders an APOD template, displaying the image in the HTML page.
    """
    apod_date = kwargs['apod_date']

    template = 'apod.html'
    ctx = {}

    try:
        # Drop if invalid date is passed in (caused by user directly editing URL)
        if not valid_date(apod_date):
            raise ValidationError(f'Invalid date provided ({apod_date}). Please use format YYYY-MM-DD and try again')

        # If this is our first call to this APOD, store the data.
        # If for any reason we have a record of this APOD, but no img URL, re-grab the data.
        apod, created = Apod.objects.get_or_create(date=apod_date)
        if created or not apod.url:

            api = get_api(date=apod_date)
            successful, resp = api.get_apod()

            # If we don't get a 200, remove new instance and throw exc:
            if not successful:
                apod.delete()
                raise Exception(resp)

            apod.url = resp.get('url')
            apod.title = resp.get('title')
            apod.copyright = resp.get('copyright', '')
            apod.explanation = resp.get('explanation', '')
            apod.hdurl = resp.get('hdurl', '')
            apod.media_type = resp.get('media_type', '')
            apod.service_version = resp.get('service_version', '')
            apod.raw_api_response = resp
            apod.save()

        ctx['apod'] = apod
        ctx['created'] = created

    # Store error messages to be rendered out on the UI
    except Exception as exc:
        error_msg = f'Error - {exc}'
        messages.error(request, error_msg)
        return redirect(f'/apod/{TODAY}')

    except ValidationError as ve:
        validation_error = f'Validation Error - {ve}'
        messages.error(request, validation_error)
        return redirect(f'/apod/{TODAY}')

    return render(request, template, ctx)
