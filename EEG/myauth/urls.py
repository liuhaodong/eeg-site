from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^googleTokenReceiver$', 'EEG.myauth.views.googleTokenReceiver', name = 'tokengoogle'),
)
