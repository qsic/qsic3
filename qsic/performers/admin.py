from django.contrib import admin

from image_cropping import ImageCroppingMixin

from .models import Performer


class PerformerAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'it_url',)
    search_fields = ('first_name', 'last_name', 'it_id',)
admin.site.register(Performer, PerformerAdmin)