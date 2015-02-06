from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^profhome$', 'EEG.prof.views.profhome', name = 'profhome'),
    url(r'^course/(.*)$','EEG.prof.views.course',name='course'),
    url(r'^add_course$', 'EEG.prof.views.add_course', name = 'course_add'),
    url(r'^add_lecture/(.*)$', 'EEG.prof.views.add_lecture', name = 'lecture_add'),
    url(r'^add_video_lecture/(.*)$', 'EEG.prof.views.add_video_lecture', name = 'video_lecture_add'),
    url(r'^add_video_series/(.*)$', 'EEG.prof.views.add_video_series', name = 'video_series_add'),
    url(r'^show_series/(.*)$', 'EEG.prof.views.show_series', name = 'show_series'),
)
