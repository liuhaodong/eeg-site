from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^market/home$', 'EEG.nm.views.home'),
    url(r'^market/cg/(.*)$', 'EEG.nm.views.content_group'),
    url(r'^market/delete/(.*)$', 'EEG.nm.views.delete'),
    url(r'^market/rename/(.*)$', 'EEG.nm.views.rename'),
    url(r'^market/clear/(.*)$', 'EEG.nm.views.clear'),
    url(r'^market/setup/(.*)$', 'EEG.nm.views.setup_experiment'),
    url(r'^add_campaign$', 'EEG.nm.views.add_campaign'),
    url(r'^add_content/(.*)$', 'EEG.nm.views.add_content'),
    url(r'^add_video/(.*)$', 'EEG.nm.views.add_video'),
    url(r'^add_series/(.*)$', 'EEG.nm.views.add_video_series'),
    url(r'^market/experiment/(.*)$', 'EEG.nm.views.experiment'),
    url(r'^market/game/(.*)$', 'EEG.nm.views.game'),
    url(r'^market/film/(.*)$', 'EEG.nm.views.film'),
    url(r'^market/setup_film/(.*)$', 'EEG.nm.views.setup_film'),
    url(r'^market/setup_game/(.*)$', 'EEG.nm.views.setup_game')
)
