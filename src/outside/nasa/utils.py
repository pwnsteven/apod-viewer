import datetime


# ==================================================
# Utils
# --------------------------------------------------
def valid_date(date_text):
    """ Validate the date we pass in is formatted correctly

    Used across form and view.

    expected format: YYYY-MM-DD
    """
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False