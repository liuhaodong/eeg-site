from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from rest_framework import routers
import settings
admin.autodiscover()
from EEG.account import api_views

router = routers.DefaultRouter()
router.register(r'users', api_views.UserViewSet)
router.register(r'groups', api_views.GroupViewSet)
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'EEG.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
  #  url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^EEG/', include('EEG.account.urls')),
    url(r'^EEG/', include('EEG.API.urls')),
    url(r'^EEG/', include('EEG.myauth.urls')),
    url(r'^EEG/', include('EEG.debug.urls')),
    url(r'^EEG/', include('EEG.prof.urls')),
    url(r'^EEG/', include('EEG.nm.urls')),
    url(r'^', include('EEG.site.urls')),
    url(r'^EEG/', include('EEG.student.urls')),
    url(r'^user/password/reset/$','django.contrib.auth.views.password_reset',
            {'post_reset_redirect' : '/user/password/reset/done/'},name="password_reset"),
        (r'^user/password/reset/done/$','django.contrib.auth.views.password_reset_done'),
        (r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$','django.contrib.auth.views.password_reset_confirm',
            {'post_reset_redirect' : '/user/password/done/'}),
        (r'^user/password/done/$','django.contrib.auth.views.password_reset_complete'),
)
urlpatterns += patterns('', url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
        url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_URL}), )
