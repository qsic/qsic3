from django.contrib import admin
from django.utils import timezone

from image_cropping import ImageCroppingMixin

from .models import Performer
from core.admin import QsicModelAdmin


class PerformerAdmin(ImageCroppingMixin, QsicModelAdmin):
    list_display = ('first_name', 'last_name', 'it_url', 'is_active',)
    search_fields = ('first_name', 'last_name', 'it_id',)
    extra_context = {'has_it_parser': True}

    def load_from_it(self, request, queryset):
        for obj in queryset:
            obj.load_from_it()
    load_from_it.short_description = 'Load from Improvteams.com'

    def mark_as_is_active(self, request, queryset):
        for obj in queryset:
            obj.is_active = True
            obj.save()
    mark_as_is_active.short_description = 'Mark performer(s) as active.'

    def mark_as_is_inactive(self, request, queryset):
        for obj in queryset:
            obj.is_active = False
            obj.save()
    mark_as_is_inactive.short_description = 'Mark performer(s) as inactive.'

    def mark_as_left_group(self, request, queryset):
        for obj in queryset:
            # Get all group perofrmer relations for perfomer
            gpr_qs = obj.groupperformerrelation_set.filter(end_dt=None)
            # add end dates to group performer relations without end dates
            gpr_qs.update(end_dt=timezone.now())
    mark_as_left_group.short_description = 'Mark performer(s) as "Left Group".'

    actions = [load_from_it, mark_as_is_active, mark_as_is_inactive, mark_as_left_group]
admin.site.register(Performer, PerformerAdmin)