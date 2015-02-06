from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^train_matlab$', 'EEG.matlab.views.trainMatlab',name='train_matlab'),
    url(r'^test_matlab$', 'EEG.matlab.views.testMatlab',name='test_matlab'),
)
