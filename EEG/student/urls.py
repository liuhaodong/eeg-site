from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^student/home$', 'EEG.student.views.studenthome', name='studenthome'),
    url(r'^student/course/(.*)$', 'EEG.student.views.course', name='stu_course'),
    url(r'^API/start_session$', 'EEG.student.views.start_session', name='start_session'),
    url(r'^API/stop_session$', 'EEG.student.views.stop_session', name='stop_session'),
    url(r'^API/store_answers$', 'EEG.student.views.store_answers'),
    url(r'^API/store_session_tag$', 'EEG.student.views.store_session_tag')
)
