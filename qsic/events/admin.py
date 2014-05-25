from django.contrib import admin

from image_cropping import ImageCroppingMixin

from .models import Event
from .models import Performance
from .models import PerformanceGroupPerformerRelation
from qsic.core.admin import QsicModelAdmin


class EventAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('name', 'start_dt',)
    search_fields = ('name',)
admin.site.register(Event, EventAdmin)


class PerformanceAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('name', 'event', 'start_dt', 'end_dt', 'price',)
    search_fields = ('name', 'event',)
admin.site.register(Performance, PerformanceAdmin)


class PerformanceGroupPerformerRelationAdmin(admin.ModelAdmin):
    list_display = ('performance', 'performer', 'group',)
    search_fields = ('performance', 'performer', 'group',)
admin.site.register(PerformanceGroupPerformerRelation, PerformanceGroupPerformerRelationAdmin)