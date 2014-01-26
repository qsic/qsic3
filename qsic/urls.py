from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',

    # to index page of QSIC
    #url(r'^$', 'qsic.views.index', name='qsic_index'),

    url(r'^events/', include('qsic.events.urls')),

)
