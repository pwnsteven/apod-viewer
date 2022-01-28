from django.contrib import admin
from django.db.models import JSONField
from django.utils import safestring

from prettyjson import PrettyJSONWidget

from outside.nasa import models


@admin.register(models.Apod)
class ApodAdmin(admin.ModelAdmin):

    # make the stored raw response easily readable
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget},
    }

    readonly_fields = ['created_ts', 'updated_ts']
    list_display = ['pk', '_view_on_site_link', 'title', 'media_type', 'created_ts']
    list_filter = ['media_type']

    search_fields = ['pk']
    ordering = ('-pk',)
    show_full_result_count = False

    def _view_on_site_link(self, apod):
        """Return a link to view the APOD in the UI
        """
        html = f'<a href="{apod.get_absolute_url()}">View on site</a>'
        return safestring.mark_safe(html)

    _view_on_site_link.short_description = 'View on site'
