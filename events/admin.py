from django.contrib import admin

from image_cropping import ImageCroppingMixin

from .models import Event
from .models import Performance
from .models import PerformanceGroupPerformerRelation
from .models import ReoccurringEventType
from core.admin import QsicModelAdmin


class PerformanceGroupPerformerRelationAdmin(admin.ModelAdmin):
    list_display = ('performance', 'performer', 'group',)
    search_fields = ('performance', 'performer', 'group',)
admin.site.register(PerformanceGroupPerformerRelation, PerformanceGroupPerformerRelationAdmin)


class PerformanceGroupPerformerRelationAdminInline(admin.TabularInline):
    model = PerformanceGroupPerformerRelation


class PerformanceAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('name', 'event', 'start_dt', 'end_dt', 'price',)
    search_fields = ('name', 'event',)

    inlines = [
        PerformanceGroupPerformerRelationAdminInline,
    ]

    def save_formset(self, request, form, formset, change):
        instance = form.save(commit=False)

        if not instance.name and formset.cleaned_data and formset.cleaned_data[0]:
            group = None
            if 'group' in formset.cleaned_data[0]:
                group = formset.cleaned_data[0]['group']

            if group:
                name = group.name
            else:
                name = 'Performance'

            instance.name = name
            instance.save()
        formset.save()


admin.site.register(Performance, PerformanceAdmin)


class EventAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('name', 'start_dt', 'reoccurring_event_type', 'is_placeholder')
    ordering = ('-_start_dt',)
    search_fields = ('name',)
    actions = ['mark_as_placeholder']

    def mark_as_placeholder(self, request, queryset):
        rows_updated = queryset.update(is_placeholder=True)
        self.message_user(request, "%s event(s) marked as placeholder(s)." % rows_updated)
    mark_as_placeholder.short_description = "Mark selected events as placeholders"
admin.site.register(Event, EventAdmin)


class ReoccurringEventTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'period',)
    search_fields = ('name',)
admin.site.register(ReoccurringEventType, ReoccurringEventTypeAdmin)