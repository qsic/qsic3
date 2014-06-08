from django.contrib import admin

from image_cropping import ImageCroppingMixin

from qsic.core.models import QSICPic


class QsicModelAdmin(admin.ModelAdmin):

    extra_context = None

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(self.extra_context or {})
        return super(QsicModelAdmin, self).add_view(request, form_url='', extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(self.extra_context or {})
        return super(QsicModelAdmin, self).change_view(request, object_id, form_url='', extra_context=extra_context)


class QSICPicAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('id', 'photo', 'caption',)
    search_fields = ('id', 'photo', 'caption',)
admin.site.register(QSICPic, QSICPicAdmin)