from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^dbfiller$', 'EEG.debug.views.fill_db',name='dbfiller'),
    url(r'^dump$', 'EEG.debug.views.dump',name='dump'),
    url(r'^direct_input$', 'EEG.debug.views.directInput', name = 'directInput'),
    url(r'^java_test$', 'EEG.debug.views.run_java_test', name = 'test_java'),
    url(r'^train$', 'EEG.debug.views.train_on_past_data', name = 'train_java'),
    url(r'^add_game$', 'EEG.debug.views.add_game', name = 'add_game'),
    url(r'^debug$', 'EEG.debug.views.debug', name = 'debug'),
    url(r'^load_videos$', 'EEG.debug.views.load_static_videos', name = 'load_vids'),
    url(r'^debug_add_session$', 'EEG.debug.views.add_session_endpoint', name = 'debug_add_session'),
    url(r'^debug_del_raw$', 'EEG.debug.views.del_raw_endpoint', name = 'debug_del_raw'),
)
