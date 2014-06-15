from django.contrib import admin

from image_cropping import ImageCroppingMixin

from .models import Event
from .models import Performance
from .models import PerformanceGroupPerformerRelation
from qsic.core.admin import QsicModelAdmin


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
    list_display = ('name', 'start_dt',)
    search_fields = ('name',)
admin.site.register(Event, EventAdmin)

