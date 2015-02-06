echo "Get Login Page CSRF TOKEN\n"
curl -v http://localhost:8000/EEG/login | grep -o 'value='\''[^;]*'\'''

echo "Login And GET SESSION ID\n"
curl -v --data "username=haodongl&password=123456&csrfmiddlewaretoken=uuvrUHeeSzdb6O2N2rq58gx99CkEl9r8" --cookie "csrftoken=uuvrUHeeSzdb6O2N2rq58gx99CkEl9r8" http://localhost:8000/EEG/login | grep -o 'sessionid='\''[^;]*'\'''

echo "Create Content\n"
curl -v --data "csrfmiddlewaretoken=OPGXI9lJhOoYGQGAZ9pB6dRzr5mi9jVS&name=test5" --cookie "sessionid=bav5o22c6pn3yngbqrn970vu98srhxce; csrftoken=OPGXI9lJhOoYGQGAZ9pB6dRzr5mi9jVS" http://localhost:8000/EEG/add_content/fuck   

echo "Start Session\n"
curl --data "content_group_name=fuck&content_name=hehe&csrfmiddlewaretoken=OPGXI9lJhOoYGQGAZ9pB6dRzr5mi9jVS&content_time=0&viewer_name=[\"testuser3\"]" --cookie "sessionid=bav5o22c6pn3yngbqrn970vu98srhxce; csrftoken=OPGXI9lJhOoYGQGAZ9pB6dRzr5mi9jVS" http://localhost:8000/EEG/API/start_session
