from django.contrib import admin

from image_cropping import ImageCroppingMixin

from .models import Group
from .models import GroupPerformerRelation
from qsic.core.admin import QsicModelAdmin


class GroupAdmin(ImageCroppingMixin, QsicModelAdmin):
    list_display = ('name', 'it_url', 'is_house_team', 'is_active',)
    search_fields = ('name',)
    extra_context = {'has_it_parser': True}

    def load_from_it(self, request, queryset):
        for obj in queryset:
                obj.load_from_it()
    load_from_it.short_description = 'Load from Improvteams.com'

    def mark_as_is_active(self, request, queryset):
        for obj in queryset:
            obj.is_active = True
            obj.save()
    mark_as_is_active.short_description = 'Mark group(s) as active.'

    def mark_as_is_inactive(self, request, queryset):
        for obj in queryset:
            obj.is_active = False
            obj.save()
    mark_as_is_inactive.short_description = 'Mark group(s) as inactive.'

    actions = [load_from_it, mark_as_is_active, mark_as_is_inactive]

admin.site.register(Group, GroupAdmin)


class GroupPerformerRelationAdmin(admin.ModelAdmin):
    list_display = ('group', 'performer', 'start_dt', 'end_dt',)
    search_fields = ('group', 'performer',)
admin.site.register(GroupPerformerRelation, GroupPerformerRelationAdmin)
