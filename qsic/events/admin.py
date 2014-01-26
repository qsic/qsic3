from django.contrib import admin

from .models import EventSeries
from .models import Event
from .models import Performance
from .models import PerformanceGroupPerformerRelation


class EventSeriesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
admin.site.register(EventSeries, EventSeriesAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_series', 'start_dt', 'end_dt',)
    search_fields = ('name', 'event_series',)
admin.site.register(Event, EventAdmin)


class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'start_dt', 'end_dt', 'price',)
    search_fields = ('name', 'event',)
admin.site.register(Performance, PerformanceAdmin)


class PerformanceGroupPerformerRelationAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'start_dt', 'end_dt', 'price',)
    search_fields = ('name', 'event',)
admin.site.register(PerformanceGroupPerformerRelation, PerformanceGroupPerformerRelationAdmin)