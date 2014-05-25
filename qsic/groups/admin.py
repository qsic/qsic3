from django.contrib import admin

from image_cropping import ImageCroppingMixin

from .models import Group
from .models import GroupPerformerRelation


class GroupAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('name', 'it_url',)
    search_fields = ('name',)
admin.site.register(Group, GroupAdmin)


class GroupPerformerRelationAdmin(admin.ModelAdmin):
    list_display = ('group', 'performer', 'start_dt', 'end_dt',)
    search_fields = ('group', 'performer',)
admin.site.register(GroupPerformerRelation, GroupPerformerRelationAdmin)
