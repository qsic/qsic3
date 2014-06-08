from django.contrib import admin

from image_cropping import ImageCroppingMixin

from .models import Performer
from qsic.core.admin import QsicModelAdmin


class PerformerAdmin(ImageCroppingMixin, QsicModelAdmin):
    list_display = ('first_name', 'last_name', 'it_url',)
    search_fields = ('first_name', 'last_name', 'it_id',)
    extra_context = {'has_it_parser': True}

    def load_from_it(self, request, queryset):
        for obj in queryset:
                obj.load_from_it()
    load_from_it.short_description = 'Load from Improvteams.com'

    actions = [load_from_it]
admin.site.register(Performer, PerformerAdmin)