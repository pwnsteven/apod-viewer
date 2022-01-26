"""outside URL Configuration
"""

from django.contrib import admin
from django.urls import path

from outside.nasa import views as nasa_views

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Nasa Views
    # -------------------------------------------------------------------------
    path('', nasa_views.homepage),
]
