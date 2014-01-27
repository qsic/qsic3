from django.contrib import admin

from .models import Group
from .models import GroupPerformerRelation


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'it_url',)
    search_fields = ('name',)
admin.site.register(Group, GroupAdmin)


class GroupPerformerRelationAdmin(admin.ModelAdmin):
    list_display = ('group', 'performer', 'start_dt', 'end_dt',)
    search_fields = ('group', 'performer',)
admin.site.register(GroupPerformerRelation, GroupPerformerRelationAdmin)
