from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'EEG.site.views.mainpage', name='main'),
)
