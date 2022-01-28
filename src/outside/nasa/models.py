from django.db import models
from django.urls import reverse


class Apod(models.Model):
    """ Model to store the APOD API response data """

    # Required:
    date = models.CharField(max_length=10, db_index=True, primary_key=True)  # YYYY-MM-DD
    title = models.CharField(max_length=200, db_index=True, blank=False)
    url = models.URLField(max_length=200, blank=False)

    hdurl = models.URLField(max_length=200)
    explanation = models.TextField(blank=True)
    media_type = models.CharField(max_length=200, db_index=True, blank=True)
    service_version = models.CharField(max_length=200, db_index=True, blank=True)
    copyright = models.CharField(max_length=200, db_index=True, blank=True)
    raw_api_response = models.JSONField(default=dict)

    # Audit
    created_ts = models.DateTimeField(auto_now_add=True, help_text='When the entry was added')
    updated_ts = models.DateTimeField(auto_now=True, db_index=True, help_text='When the entry was last updated')

    class Meta:
        indexes = [
            models.Index(fields=['date'])
        ]
        verbose_name = 'APOD'
        verbose_name_plural = 'APODs'

    def __str__(self):
        return f'{self.date} / {self.title}'

    def get_absolute_url(self):
        """ Render link to this specific obj
        """
        return reverse('apod', args=[self.pk])

    def get_admin_url(self):
        """ Util to return the apod admin url at the instance level
        """
        return reverse(f'admin:{self._meta.app_label}_{self._meta.model_name}_change', args=(self.pk,))

    @property
    def is_video(self):
        return bool(self.media_type == 'video')
