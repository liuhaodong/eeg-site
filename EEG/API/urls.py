from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^input$', 'EEG.API.views.input',name='input'),
    url(r'^course_list$', 'EEG.API.views.course_list', name = 'course_list'),
    url(r'^next_lecture/(.*)$', 'EEG.API.views.get_next_lecture', name = 'next_lecture'),
    url(r'^get_labels$', 'EEG.API.views.get_label_sequence', name = 'get_label_sequence'),
    url(r'^estimate_duration$', 'EEG.API.views.estimate_content_duration', name = 'estimate_duration'),
    url(r'^upload_labels$', 'EEG.API.views.upload_labels', name = 'upload_labels'),
    url(r'^check_eeg_connection$', 'EEG.API.views.check_eeg', name = 'check_eeg')
)
