from django.shortcuts import render


def homepage(request):
    """Render the homepage.
    """
    template = 'homepage.html'
    ctx = {}

    return render(request, template, ctx)


# TODO: Write a view that renders an APOD template, displaying the image in the HTML page.

