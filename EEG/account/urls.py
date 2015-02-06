from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'login.html'},name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^register$', 'EEG.account.views.register',name='register'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'EEG.account.views.confirm_registration', name='confirm'),
    url(r'^first_login$', 'EEG.account.views.first_login',name='first_login'),
)
