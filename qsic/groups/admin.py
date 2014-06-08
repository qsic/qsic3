from django.contrib import admin

from image_cropping import ImageCroppingMixin

from .models import Group
from .models import GroupPerformerRelation
from qsic.core.admin import QsicModelAdmin


class GroupAdmin(ImageCroppingMixin, QsicModelAdmin):
    list_display = ('name', 'it_url',)
    search_fields = ('name',)
    extra_context = {'has_it_parser': True}

    def load_from_it(self, request, queryset):
        for obj in queryset:
                obj.load_from_it()
    load_from_it.short_description = 'Load from Improvteams.com'

    actions = [load_from_it]

admin.site.register(Group, GroupAdmin)


class GroupPerformerRelationAdmin(admin.ModelAdmin):
    list_display = ('group', 'performer', 'start_dt', 'end_dt',)
    search_fields = ('group', 'performer',)
admin.site.register(GroupPerformerRelation, GroupPerformerRelationAdmin)
